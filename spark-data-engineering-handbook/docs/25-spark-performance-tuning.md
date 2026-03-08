# Chapter 25 – Spark Performance Tuning Guide

Spark performance tuning involves optimizing:

* cluster resources
* memory usage
* partitioning
* joins
* shuffle operations
* query execution

Efficient tuning can reduce job execution time **from hours to minutes**.

---

# 1️⃣ Spark Performance Tuning Layers

Spark performance depends on multiple layers.

| Layer   | Optimization Area      |
| ------- | ---------------------- |
| Cluster | number of executors    |
| Memory  | executor memory        |
| Data    | partitioning           |
| Compute | task parallelism       |
| Query   | Catalyst optimizations |

---

# 2️⃣ Increase Parallelism

Spark processes data in **partitions**.

More partitions allow more parallel tasks.

Example:

```python
df = df.repartition(200)
```

Recommended rule:

```text
Number of partitions ≈ 2–3 × total CPU cores
```

Example cluster:

| Executors | Cores per Executor | Total Cores |
| --------- | ------------------ | ----------- |
| 5         | 4                  | 20          |

Recommended partitions:

```text
40–60 partitions
```

---

# 3️⃣ Avoid Small Files Problem

Many small files create many tasks.

Example:

```text
10,000 files → 10,000 tasks
```

Problems:

* scheduler overhead
* slow job start

Solution:

```python
df.coalesce(10).write.parquet("output")
```

---

# 4️⃣ Use Broadcast Joins

If one dataset is small, broadcast it.

Example:

```python
from pyspark.sql.functions import broadcast

df1.join(broadcast(df2), "id")
```

Benefits:

```text
No shuffle
Faster joins
Less network traffic
```

---

# 5️⃣ Filter Early

Always reduce dataset size before heavy operations.

Example:

Bad pipeline:

```python
df.join(customers).filter("amount > 100")
```

Better pipeline:

```python
df.filter("amount > 100").join(customers)
```

This reduces shuffle data.

---

# 6️⃣ Handle Data Skew

Data skew causes one executor to process most data.

Example skew:

```text
Partition 1 → 90% data
Partition 2 → 5%
Partition 3 → 5%
```

Solutions:

* salting
* repartition
* AQE skew handling

Example:

```python
df = df.repartition(200)
```

---

# 7️⃣ Avoid collect() on Large Data

Bad example:

```python
df.collect()
```

This sends **all data to driver memory**.

Better alternatives:

```python
df.show()
df.take(10)
df.write.parquet("output")
```

---

# 8️⃣ Use Cache for Repeated Data

If dataset is reused multiple times:

```python
df.cache()
```

Example:

```python
filtered = df.filter("amount > 100").cache()

filtered.count()
filtered.groupBy("country").count()
```

Without cache Spark recomputes transformations.

---

# 9️⃣ Choose Correct File Format

Columnar formats improve performance.

Recommended formats:

| Format  | Advantage             |
| ------- | --------------------- |
| Parquet | column pruning        |
| ORC     | optimized compression |
| Delta   | ACID transactions     |

Avoid:

```text
CSV
JSON
```

for large-scale processing.

---

# 🔟 Use Predicate Pushdown

Example:

```python
df.filter("age > 30")
```

Spark pushes filter to storage layer.

Benefits:

```text
Less data read
Faster query execution
```

---

# 1️⃣1️⃣ Optimize Shuffle

Shuffle is the **most expensive Spark operation**.

Caused by:

```text
groupBy
join
distinct
reduceByKey
```

To optimize:

* reduce shuffle data
* use broadcast join
* increase partitions

---

# 1️⃣2️⃣ Tune Executor Configuration

Example configuration:

```bash
spark-submit \
--num-executors 6 \
--executor-cores 4 \
--executor-memory 16G
```

Guidelines:

| Parameter       | Recommendation        |
| --------------- | --------------------- |
| Executor cores  | 3–5 cores             |
| Executor memory | based on dataset size |

---

# 1️⃣3️⃣ Use Adaptive Query Execution (AQE)

AQE dynamically optimizes queries.

Enable:

```bash
spark.sql.adaptive.enabled=true
```

Benefits:

* dynamic join optimization
* skew handling
* partition coalescing

---

# 1️⃣4️⃣ Monitor Spark UI

Spark UI helps identify performance bottlenecks.

Important metrics:

| Metric        | Meaning          |
| ------------- | ---------------- |
| Shuffle Read  | network transfer |
| Shuffle Spill | memory overflow  |
| Task Duration | slow tasks       |

Slow tasks usually indicate:

* data skew
* memory pressure

---

# 1️⃣5️⃣ Real Production Example

Dataset:

```text
1 TB transaction data
```

Initial job runtime:

```text
3 hours
```

After tuning:

* broadcast join
* partition optimization
* caching

New runtime:

```text
25 minutes
```

---

# 1️⃣6️⃣ Spark Tuning Checklist

Before running production jobs check:

```text
✔ partitions optimized
✔ broadcast joins used
✔ shuffle minimized
✔ caching used properly
✔ no large collect()
✔ AQE enabled
```

---

# Interview Questions

### What causes slow Spark jobs?

Large shuffle operations, data skew, insufficient partitions.

---

### How can Spark performance be improved?

Using broadcast joins, partition tuning, caching, and AQE.

---

### What is the most expensive Spark operation?

Shuffle.

---

# Key Takeaway

Spark performance tuning focuses on optimizing:

```text
Partitioning
Shuffle operations
Join strategies
Memory usage
Cluster configuration
```

Mastering these techniques allows engineers to **build highly efficient big data pipelines**.

---
