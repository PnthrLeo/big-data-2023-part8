import argparse

import findspark
from pyspark import SparkContext
from pyspark.sql import SparkSession

from database.database import Database
from preprocessing import load_csv_data

findspark.add_packages(["com.microsoft.azure:spark-mssql-connector_2.12:1.3.0-BETA"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='../data/openfoods.csv')
    parser.add_argument('--data_name', default='openfoods')
    args = parser.parse_args()

    spark = SparkSession.builder \
        .appName('KMeansClustering') \
        .config('spark.num.executors', '2') \
        .config('spark.executor.cores', '5') \
        .config('spark.executor.memory', '5g') \
        .config('spark.driver.memory', '5g') \
        .getOrCreate()

    df = load_csv_data(spark, args.data_path)
    
    database = Database()
    database.set_data(df, 'data', args.data_name)
    spark.stop()
