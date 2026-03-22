# Driver-Executor Model

## ✅ What you need to say in interview

- **Driver:** Single JVM process that **runs your main()**, builds the **logical plan and DAG**, splits work into **stages and tasks**, and schedules them. Also **collects results** back to the driver.
- **Executor:** JVM processes on **worker nodes** that **run tasks**, store **cached/persisted data**, and hold **shuffle output**.
- **Cluster Manager** (YARN, K8s, Databricks): Allocates resources and launches driver/executors.

## ⚙️ How it actually works

1. Driver submits application; cluster manager allocates resources.
2. Executors register with driver.
3. Driver sends tasks to executors; executors run and report back.
4. Shuffle: executors write shuffle files to disk; other executors read them.
5. Driver collects final results (e.g., `collect()`, `show()`).

## ✅ When to use

- Understanding architecture for debugging (OOM on driver vs executor).
- Explaining why `collect()` is dangerous (driver memory).
- Designing cluster sizing (driver vs executor memory).

## ❌ When to NEVER use

- Don't say "driver does the computation" — executors do.
- Don't confuse driver memory with executor memory.

## 🚩 Common interview pitfalls

- Saying executor and worker are the same (worker = node; executor = JVM process on that node).
- Forgetting that driver is single point of failure.

## 💻 Working example (PySpark)

```python
# Driver runs this
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet("/data/")        # Driver plans; executor reads
result = df.filter("amount > 100").count()  # Executor runs; driver gets count
# result collected to driver
```

## ❔ Actual interview questions + ideal answers

**Q: What is the difference between driver and executor?**

- **Junior:** Driver plans the job, executors run the tasks.
- **Senior:** Driver is a single JVM that maintains application state, builds the DAG, schedules stages, and coordinates executors. Executors are JVMs on workers that execute tasks, hold cached data, and perform shuffles. **Driver is single point of failure**; executor failure is handled by task retry.

**Q: Why would you get OOM on driver vs executor?**

- **Junior:** Driver OOM when collecting too much data; executor OOM when processing large partitions.
- **Senior:** **Driver OOM:** `collect()`, `take(n)` with large n, broadcasting huge tables, or accumulating results. **Executor OOM:** Large shuffle reads, skew causing one partition to hold too much data, or insufficient executor memory for joins/aggregations.

---

## 5-Minute Revision Cheat Sheet

- Driver: 1 JVM, plans DAG, schedules, collects.
- Executor: N JVMs, run tasks, cache, shuffle.
- `collect()` → driver memory risk.
- Worker = node; executor = JVM on worker.
