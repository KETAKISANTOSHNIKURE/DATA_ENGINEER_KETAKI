# Chapter 02 – What is Apache Spark

Apache Spark is an open-source distributed computing engine designed for large-scale data processing.

Spark supports:

* batch processing
* streaming
* machine learning
* graph analytics

---

## Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Example").getOrCreate()

data = spark.read.csv("sales.csv", header=True)

data.groupBy("country").count().show()
```

Spark automatically distributes computation across cluster nodes.

---

## Spark Execution Model

```mermaid
flowchart LR
Code --> Driver
Driver --> ClusterManager
ClusterManager --> Worker
Worker --> Executor
Executor --> Tasks
```

---

## Interview Question

Why is Spark faster than traditional Hadoop?

Answer:

Spark performs **in-memory processing and DAG optimization**.

---

⬅️ [Previous: Introduction](./01-introduction.md)
➡️ [Next: Spark vs Hadoop MapReduce](./03-spark-vs-hadoop-mapreduce.md)
