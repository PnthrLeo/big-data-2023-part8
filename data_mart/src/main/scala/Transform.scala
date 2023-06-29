package datamart

import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions._
import org.apache.spark.ml.feature.{StandardScaler, VectorAssembler}
import org.apache.spark.sql.types.FloatType


object Transforms {
    val useless_columns = List("code", "url", "creator", "created_t", 
                           "created_datetime", "last_modified_t",
                           "last_modified_datetime", "last_modified_by",
                           "product_name", "brands", "brands_tags", 
                           "countries", "countries_en", "countries_tags",
                           "states", "states_tags", "states_en",
                           "last_image_t", "last_image_datetime", 
                           "image_url", "image_small_url", 
                           "image_ingredients_url", "image_ingredients_small_url",
                           "image_nutrition_url", "image_nutrition_small_url")

    val cat_columns = List("pnns_groups_1", "pnns_groups_2", "ecoscore_grade")

    val feature_vector_col = "features"
    val scaled_feature_vector_col = "scaled_features"

    def drop_useless_cols(df: DataFrame): DataFrame = {
        return df.drop(useless_columns:_*)
    }

    def drop_cols_with_nans(df: DataFrame, threshold: Double = 0.5): DataFrame = {
        val total_rows = df.count()
        val nan_counts = df.select(df.columns.map(c => count(when(isnan(col(c)) || col(c).isNull, 1)).alias(c)): _*).first()
        val cols_to_drop = df.columns.filter { col_name =>
            val nan_count = nan_counts.getAs[Long](col_name)
            nan_count.toDouble / total_rows > threshold
        }
        return df.drop(cols_to_drop:_*)
    }

    def drop_rows_with_nans(df: DataFrame): DataFrame = {
        return df.na.drop()
    }

    def apply_one_hot_encoding(df: DataFrame): DataFrame = {
        var new_df = df
        for (col <- cat_columns) {
            val distinct_values = df.select(col).distinct().collect()
            for (value <- distinct_values) {
                new_df = new_df.withColumn(s"${col}_${value(0)}", when(df(col) === value(0), 1).otherwise(0))
            }
        }
        return new_df.drop(cat_columns:_*)
    }

    def add_feature_vector(df: DataFrame): DataFrame = {
        val new_df = df.select(df.columns.map(c => col(c).cast(FloatType).alias(c)): _*)
        val vector_assemble = new VectorAssembler().setInputCols(new_df.columns).setOutputCol(feature_vector_col)
        return vector_assemble.transform(new_df)
    }

    def apply_standard_scaling_to_feature_vector(df: DataFrame): DataFrame = {
        val standard_scaler = new StandardScaler().setInputCol(feature_vector_col).setOutputCol(scaled_feature_vector_col)
        return standard_scaler.fit(df).transform(df)
    }

    def transform_data(df: DataFrame): DataFrame = {
        var new_df = df
        new_df = drop_useless_cols(new_df)
        new_df = drop_cols_with_nans(new_df)
        new_df = drop_rows_with_nans(new_df)
        new_df = apply_one_hot_encoding(new_df)
        new_df = add_feature_vector(new_df)
        new_df = apply_standard_scaling_to_feature_vector(new_df)
        return new_df
    }
}
