import argparse
from pyspark.sql import SparkSession

from preprocessing import load_csv_data, transform_data
from models import CustomKMeans
from utils.spark import keep_spark_web_ui_alive


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path', default='../data/openfoods.csv')
    parser.add_argument('--save_model_path', default='../output/kmeans.model')
    parser.add_argument('--k', default=2)
    parser.add_argument('--random_seed', default=42)
    args = parser.parse_args()

    spark = SparkSession.builder \
        .appName('KMeansClustering') \
        .config('spark.num.executors', '2') \
        .config('spark.executor.cores', '5') \
        .config('spark.executor.memory', '5g') \
        .config('spark.driver.memory', '5g') \
        .getOrCreate()

    df = load_csv_data(spark, args.train_path)
    df = transform_data(df)

    trainer = CustomKMeans({'k': args.k, 'random_seed': args.random_seed})
    trainer.fit(df)
    trainer.transform(df)
    trainer.save_model(args.save_model_path)

    keep_spark_web_ui_alive()
    spark.stop()
