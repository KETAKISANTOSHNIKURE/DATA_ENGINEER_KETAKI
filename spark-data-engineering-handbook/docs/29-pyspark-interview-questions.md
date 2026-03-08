# Chapter 29 – PySpark Interview Questions (50 Questions)

This chapter contains commonly asked PySpark interview questions used by companies when hiring data engineers.

Topics covered:

- Spark fundamentals
- execution architecture
- performance tuning
- joins
- memory management
- distributed computing

---

## 1️⃣ Basic Spark Questions

### 1. What is Apache Spark?

Apache Spark is a distributed computing engine used for large-scale data processing. It performs computations across clusters using in-memory processing.

### 2. What are the main components of Spark?

Spark ecosystem includes:

| Component | Description |
|-----------|-------------|
| Spark Core | distributed execution engine |
| Spark SQL | structured data processing |
| MLlib | machine learning |
| GraphX | graph analytics |
| Spark Streaming | real-time processing |

### 3. What is SparkSession?

SparkSession is the entry point for Spark applications.

Example:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("demo").getOrCreate()
```

### 4. Difference between SparkContext and SparkSession?

| Feature | SparkContext | SparkSession |
|---------|--------------|--------------|
| Purpose | core Spark connection | unified API |
| Introduced | Spark 1.x | Spark 2.x |
| Supports SQL | No | Yes |

### 5. What is RDD?

RDD (Resilient Distributed Dataset) is a fault-tolerant distributed collection of objects.

---

## 2️⃣ Transformations and Actions

### 6. What is a transformation?

Transformations create new datasets. Examples: `map`, `filter`, `flatMap`

### 7. What is an action?

Actions trigger execution. Examples: `collect`, `count`, `show`, `save`

### 8. What is lazy evaluation?

Spark delays execution until an action is called. Example: `df.filter("age > 30")` – execution happens only when an action like `.show()` runs.

### 9. Difference between narrow and wide transformation?

| Type | Description |
|------|-------------|
| Narrow | no shuffle required |
| Wide | shuffle required |

Example: Narrow → `map`, Wide → `groupBy`

### 10. What is DAG in Spark?

DAG stands for Directed Acyclic Graph. It represents the execution plan of Spark transformations.

---

## 3️⃣ Spark Architecture

### 11. What is the driver?

The driver is the program that controls Spark execution. Responsibilities: create SparkSession, schedule tasks, manage DAG.

### 12. What are executors?

Executors run tasks on worker nodes. They perform actual data processing.

### 13. What is a cluster manager?

Cluster manager allocates resources to Spark applications. Examples: YARN, Kubernetes, Standalone.

### 14. What are jobs, stages, and tasks?

| Level | Description |
|-------|-------------|
| Job | triggered by action |
| Stage | separated by shuffle |
| Task | processes one partition |

---

## 4️⃣ Partitioning

### 15. What is partitioning in Spark?

Partitioning divides data into smaller pieces processed in parallel.

### 16. Difference between repartition and coalesce?

| Method | Shuffle | Use Case |
|--------|---------|----------|
| Repartition | Yes | increase partitions |
| Coalesce | No | reduce partitions |

### 17. What is the recommended partition count?

Rule: **2–3 × total CPU cores**

---

## 5️⃣ Joins

### 18. What is shuffle join?

Shuffle join redistributes data across nodes. Example: `df1.join(df2, "id")`

### 19. What is broadcast join?

Broadcast join sends a small dataset to all executors. Example:

```python
from pyspark.sql.functions import broadcast
df1.join(broadcast(df2), "id")
```

### 20. When should broadcast join be used?

When one dataset is small.

---

## 6️⃣ Performance Optimization

### 21. What is caching?

Caching stores datasets in memory. Example: `df.cache()`

### 22. What is persistence?

Persistence allows storing datasets in different storage levels. Example: `df.persist()`

### 23. What causes slow Spark jobs?

Common causes: shuffle operations, data skew, insufficient partitions.

### 24. What is data skew?

Data skew occurs when partitions contain uneven data. Example: Partition 1 → 90% data, Partition 2 → 10%

---

## 7️⃣ Memory Management

### 25. What is executor memory?

Executor memory is memory allocated to Spark executors.

### 26. What is unified memory management?

Spark shares memory between execution and storage operations.

### 27. What causes Executor Out Of Memory errors?

Common reasons: large shuffles, large joins, large partitions.

---

## 8️⃣ Spark SQL

### 28. What is Spark SQL?

Spark SQL processes structured data using SQL and DataFrames.

### 29. What is Catalyst Optimizer?

Catalyst is Spark's query optimization engine.

### 30. What is predicate pushdown?

Filters are pushed to the data source to reduce data reading.

---

## 9️⃣ Shuffle

### 31. What is shuffle?

Shuffle redistributes data across executors.

### 32. Why is shuffle expensive?

Because data must be: written to disk, transferred over network, re-partitioned.

---

## 🔟 Advanced Concepts

### 33. What is Adaptive Query Execution?

AQE dynamically optimizes queries during runtime.

### 34. What is salting in Spark?

Salting distributes skewed data across partitions.

### 35. What is Dynamic Partition Pruning?

Spark avoids scanning unnecessary partitions.

---

## 1️⃣1️⃣ Spark Internals

### 36. What is Tungsten engine?

Tungsten optimizes Spark execution using CPU-efficient memory management.

### 37. What is the role of DAG Scheduler?

It converts jobs into stages.

### 38. What is Task Scheduler?

It assigns tasks to executors.

---

## 1️⃣2️⃣ Production Questions

### 39. How do you debug a slow Spark job?

Steps: check Spark UI, analyze shuffle stages, detect data skew.

### 40. What metrics are important in Spark UI?

| Metric | Meaning |
|--------|---------|
| Task duration | slow tasks |
| Shuffle read | network data |
| Spill | memory overflow |

---

## 1️⃣3️⃣ Real Scenario Questions

### 41. How would you process 1 TB dataset?

Use: distributed cluster, partitioned processing, optimized joins.

### 42. How do you handle small files problem?

Use: `df.coalesce(10)`

### 43. Why avoid collect()?

It brings all data to driver memory.

---

## 1️⃣4️⃣ Streaming Questions

### 44. What is Spark Streaming?

Spark Streaming processes real-time data streams.

### 45. What is structured streaming?

Structured streaming processes streaming data using DataFrame APIs.

---

## 1️⃣5️⃣ Practical Questions

### 46. How do you monitor Spark jobs?

Using: Spark UI, logs, cluster metrics.

### 47. What file formats are best for Spark?

Best formats: Parquet, ORC, Delta.

### 48. Why is Parquet preferred?

Because it is columnar and supports compression.

### 49. How does Spark achieve fault tolerance?

Using RDD lineage.

### 50. What is the biggest performance improvement technique?

Reducing shuffle operations.

---

## Key Takeaway

Successful Spark engineers understand:

- Spark architecture
- Distributed execution
- Memory management
- Performance tuning

Mastering these concepts allows engineers to build efficient large-scale data processing systems.
