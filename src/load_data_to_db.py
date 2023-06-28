import argparse
import findspark
from pyspark.sql import SparkSession


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
        .config("spark.jars", "../data_mart/target/scala-2.12/data-mart_2.12-1.0.jar") \
        .getOrCreate()
        
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')
    
    sc._jvm.datamart.DataMart.set_data_for_kmeans(args.data_path, args.data_name)
    spark.stop()
