# Chapter 02 — What is Apache Spark

Apache Spark is a distributed computing engine used for processing large datasets.

---

## Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Example").getOrCreate()

data = spark.read.csv("data.csv")

data.show()
```

---

## Spark Execution Model

```mermaid
flowchart LR

Code --> Driver
Driver --> ClusterManager
ClusterManager --> Worker
Worker --> Executor
Executor --> Task
```
