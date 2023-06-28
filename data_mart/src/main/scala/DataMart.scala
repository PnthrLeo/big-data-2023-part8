package datamart

import datamart.Database
import datamart.Transforms
import datamart.EnvReader

object DataMart {
    private val _config = new EnvReader()

    def set_data_for_kmeans(csv_path: String, data_name: String): Unit = {
        val db = new Database(_config)
        val df = db.spark.read.option("sep", "\t").option("header", "true").csv(csv_path)
        db.set_data(df, "data", data_name)
    }
    
    def get_data_for_kmeans(data_name: String): org.apache.spark.sql.DataFrame = {
        val db = new Database(_config)
        val df = db.get_data("data", data_name)
        val df_transformed = Transforms.transform_data(df)
        return df_transformed
    }

    def set_experiments_data(df: org.apache.spark.sql.DataFrame, experiment_name: String): Unit = {
        val db = new Database(_config)
        db.set_data(df, "experiments", experiment_name)
    }

    def get_experiments_data(experiment_name: String): org.apache.spark.sql.DataFrame = {
        val db = new Database(_config)
        val df = db.get_data("experiments", experiment_name)
        return df
    }
}
