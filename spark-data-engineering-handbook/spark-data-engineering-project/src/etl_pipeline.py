import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spark_session import create_spark
from transform import clean_data, aggregate_revenue
import config


def run_pipeline():
    spark = create_spark()

    df = spark.read.csv(
        config.INPUT_PATH,
        header=True,
        inferSchema=True
    )

    cleaned = clean_data(df)
    revenue = aggregate_revenue(cleaned)

    revenue.show()

    revenue.write.mode("overwrite").parquet(config.OUTPUT_PATH)

    spark.stop()


if __name__ == "__main__":
    run_pipeline()
