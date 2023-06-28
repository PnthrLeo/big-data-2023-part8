import argparse

import findspark
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame

from configs import feature_vector_col, scaled_feature_vector_col
from models import CustomKMeans
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
        .config("spark.jars", "../data_mart/target/scala-2.12/data-mart_2.12-1.0.jar") \
        .getOrCreate()

    sc = spark.sparkContext
    sc.setLogLevel('ERROR')
    
    jdf = sc._jvm.datamart.DataMart.get_data_for_kmeans(args.data_name)
    df = DataFrame(jdf, spark)

    trainer = CustomKMeans({'k': args.k, 'random_seed': args.random_seed})
    trainer.fit(df)
    res_df = trainer.transform(df)
    res_df = res_df.drop(feature_vector_col, scaled_feature_vector_col)
    
    jres_df = res_df._jdf
    sc._jvm.datamart.DataMart.set_experiments_data(jres_df, args.experiment_name)
    
    trainer.save_model(args.save_model_path)

    keep_spark_web_ui_alive()
    spark.stop()
