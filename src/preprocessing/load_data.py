from pyspark.sql import SparkSession, DataFrame


def load_csv_data(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.csv(path, header=True, sep='\t')
