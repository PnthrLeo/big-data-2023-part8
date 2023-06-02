import pyspark.sql.functions as F
from pyspark.ml.feature import StandardScaler, VectorAssembler
from pyspark.sql import DataFrame
from pyspark.sql.types import FloatType

from configs import (cat_columns, feature_vector_col,
                     scaled_feature_vector_col, useless_columns)


def drop_useless_cols(df: DataFrame) -> DataFrame:
    return df.drop(*useless_columns)


def drop_cols_with_nans(df: DataFrame, threshold: float=0.5) -> DataFrame:
    number_of_records = df.count()
    nan_in_cols = df.select([F.count(F.when(F.isnan(c) | F.col(c).isNull(), c)).alias(c) for c in df.columns]).first()
    cols_to_drop = [c for c in nan_in_cols.asDict() if nan_in_cols[c] > number_of_records * threshold]
    return df.drop(*cols_to_drop)


def drop_rows_with_nans(df: DataFrame) -> DataFrame:
    return df.na.drop()


def apply_one_hot_encoding(df: DataFrame) -> DataFrame:
    for col in cat_columns:
        distinct_values = df.select(col).distinct().collect()
        for val in distinct_values:
            df = df.withColumn('{}_{}'.format(col, val), F.when((df[col] == val[0]), 1).otherwise(0))
    return df.drop(*cat_columns)


def add_feature_vector(df: DataFrame) -> DataFrame:
    df = df.select(
        *[F.col(col).cast(FloatType()).alias(col) for col in df.columns]
    )
    vector_assemble = VectorAssembler(inputCols=df.columns, outputCol=feature_vector_col)
    return vector_assemble.transform(df)


def apply_standard_scaling_to_feature_vector(df: DataFrame) -> DataFrame:
    standard_scaler = StandardScaler(
        inputCol=feature_vector_col,
        outputCol=scaled_feature_vector_col
    )
    return standard_scaler.fit(df).transform(df)  


def transform_data(df: DataFrame) -> DataFrame:
    df = drop_useless_cols(df)
    df = drop_cols_with_nans(df)
    df = drop_rows_with_nans(df)
    df = apply_one_hot_encoding(df)
    df = add_feature_vector(df)
    df = apply_standard_scaling_to_feature_vector(df)
    return df
    