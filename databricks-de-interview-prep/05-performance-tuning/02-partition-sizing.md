# Partition Sizing

## ✅ What you need to say in interview

- **Target:** ~**128MB–200MB** per partition. Balances parallelism and overhead.
- **Formula:** `partitions ≈ total_data_size / 128MB`. Also consider **2–4× cores** for CPU-bound.
- **Too few:** Underutilization, large tasks, OOM risk. **Too many:** Scheduling overhead, small tasks, many small files.
- **Databricks:** Default often 200; tune based on data size.

## ⚙️ How it actually works

- Each partition = one task. More partitions = more tasks = more parallelism but more overhead.
- Small partitions: quick tasks, but scheduling + metadata overhead.
- Large partitions: fewer tasks, risk of OOM or long tail.

## ✅ When to use

- After reading; before shuffle-heavy ops.
- When writing—control output file count.
- Debugging slow jobs—check partition count and size.

## ❌ When to NEVER use

- Don't use fixed partition count (e.g., 200) regardless of data size.
- Don't create millions of partitions—overhead.
- Don't ignore partition size when debugging OOM.

## 🚩 Common interview pitfalls

- Recommending "200 partitions" without context.
- Not differentiating: input partitions vs shuffle partitions vs output partitions.

## 💻 Working example (SQL + PySpark)

```python
# Size-based
num_partitions = int(df.rdd.size() / (128 * 1024 * 1024))  # approx
df = df.repartition(max(1, num_partitions))

# Or by cores
df = df.repartition(sc.defaultParallelism * 2)

# Before write
df.coalesce(10).write.parquet("/out/")  # 10 files
```

## ❔ Actual interview questions + ideal answers

**Q: What is a good partition size?**

- **Junior:** Around 128MB. 2–3x cores for partition count.
- **Senior:** **128MB–200MB per partition** is a common target. Formula: `partitions = total_data_size / 128MB`. For CPU-bound: **2–4× core count**. Too small = overhead; too large = OOM or stragglers. **After shuffle**, AQE can coalesce small partitions. For **writes**, balance file count (coalesce) with downstream read parallelism.

**Q: How do you determine partition count for a 10GB dataset?**

- **Junior:** 10GB / 128MB ≈ 80 partitions.
- **Senior:** **10GB / 128MB ≈ 80 partitions.** Also check **cluster size**—if 20 cores, 80 is 4× parallelism, reasonable. Use `repartition(80)` or let Spark/AQE handle it. For **output**, consider downstream consumers—80 files may be fine; if too many small files, coalesce before write.

---

## 5-Minute Revision Cheat Sheet

- 128–200MB per partition.
- partitions ≈ size / 128MB.
- 2–4× cores for CPU-bound.
- Too few = underuse; too many = overhead.
