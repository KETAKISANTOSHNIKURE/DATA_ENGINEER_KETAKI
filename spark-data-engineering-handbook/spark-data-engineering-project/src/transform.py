from pyspark.sql.functions import col, sum


def clean_data(df):
    df = df.filter(col("price") > 0)
    return df


def aggregate_revenue(df):
    revenue = df.groupBy("country").agg(sum("price").alias("revenue"))
    return revenue
