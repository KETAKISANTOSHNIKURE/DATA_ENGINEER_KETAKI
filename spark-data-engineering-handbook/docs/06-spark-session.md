# Chapter 06 – SparkSession

`SparkSession` is the **entry point to all Spark functionality**.

It allows you to work with:

* DataFrames
* Spark SQL
* Structured Streaming
* Spark configuration

Before Spark 2.0, developers used multiple contexts like:

* SparkContext
* SQLContext
* HiveContext

Spark 2.0 unified them into **SparkSession**.

---

# 1️⃣ Why SparkSession Was Introduced

Before Spark 2.0:

```python
sc = SparkContext()
sqlContext = SQLContext(sc)
hiveContext = HiveContext(sc)
```

Managing multiple contexts created complexity.

Spark introduced **SparkSession** to unify them.

---

# 2️⃣ Creating SparkSession

Example:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSessionExample") \
    .getOrCreate()
```

Explanation:

| Metho
