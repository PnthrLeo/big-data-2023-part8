import argparse

import findspark
from pyspark.sql import SparkSession

from configs import feature_vector_col, scaled_feature_vector_col
from database.database import Database
from models import CustomKMeans
from preprocessing import transform_data
from utils.spark import keep_spark_web_ui_alive

findspark.add_packages(["com.microsoft.azure:spark-mssql-connector_2.12:1.3.0-BETA"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_name', default='openfoods')
    parser.add_argument('--save_model_path', default='../output/kmeans.model')
    parser.add_argument('--k', default=2)
    parser.add_argument('--random_seed', default=42)
    parser.add_argument('--experiment_name', default='test')
    args = parser.parse_args()

    spark = SparkSession.builder \
        .appName('KMeansClustering') \
        .config('spark.num.executors', '2') \
        .config('spark.executor.cores', '5') \
        .config('spark.executor.memory', '5g') \
        .config('spark.driver.memory', '5g') \
        .getOrCreate()

    database = Database()
    df = database.get_data(spark, 'data', args.data_name)
    
    df = transform_data(df)

    trainer = CustomKMeans({'k': args.k, 'random_seed': args.random_seed})
    trainer.fit(df)
    res_df = trainer.transform(df)
    res_df = res_df.drop(feature_vector_col, scaled_feature_vector_col)
    
    database.set_data(res_df, 'experiments', args.experiment_name)
    
    trainer.save_model(args.save_model_path)

    keep_spark_web_ui_alive()
    spark.stop()
