# Partitions, coalesce, repartition

## ✅ What you need to say in interview

- **Partition:** Logical chunk of data; one partition = one task. More partitions = more parallelism, but overhead if too many.
- **repartition(n):** **Redistributes** data into n partitions. **Always does a full shuffle.** Use to **increase** partitions.
- **coalesce(n):** **Merges** partitions into n. **No shuffle** when reducing. Use to **reduce** partitions (e.g., before write to avoid small files).

## ⚙️ How it actually works

- `repartition`: Hash-partitions data; full shuffle. Even distribution.
- `coalesce`: Combines adjacent partitions. When reducing, no shuffle—each partition stays on its executor, partitions are merged locally. Cannot increase partitions.

## ✅ When to use

- **repartition:** Increase parallelism, fix skew (with custom key), before heavy shuffle.
- **coalesce:** Reduce partitions before write, avoid small-file problem.

## ❌ When to NEVER use

- Don't use `repartition` to reduce partitions before write—use `coalesce` to avoid unnecessary shuffle.
- Don't coalesce to 1 before a wide transformation—creates a single bottleneck.
- Don't create millions of partitions—task scheduling overhead.

## 🚩 Common interview pitfalls

- Saying coalesce does a shuffle.
- Recommending fixed partition count (e.g., 200) without considering data size—aim for ~128MB–200MB per partition.

## 💻 Working example (PySpark)

```python
# Increase partitions (shuffle)
df.repartition(200)

# Reduce partitions (no shuffle)
df.coalesce(10)

# Repartition by column (for join/groupBy)
df.repartition("region")

# Before write — coalesce to limit output files
df.coalesce(4).write.parquet("/out/")
```

```sql
-- SQL
SELECT * FROM table DISTRIBUTE BY region;  -- repartition by column
```

## ❔ Actual interview questions + ideal answers

**Q: When do you use repartition vs coalesce?**

- **Junior:** Repartition to increase partitions, coalesce to reduce. Coalesce doesn't shuffle.
- **Senior:** **repartition** when you need to **increase** partitions or **redistribute** by key—it shuffles. **coalesce** when **reducing** partitions—e.g., before writing to avoid small files. Coalesce **does not shuffle** when going from more to fewer partitions; it merges partitions locally. Use coalesce for the common "reduce before write" case.

**Q: What is a good number of partitions?**

- **Junior:** 2–3x the number of cores.
- **Senior:** Target **~128MB–200MB per partition** for optimal task size. Rule of thumb: `total_data_size / 128MB`. Also consider **2–4x cores** for CPU-bound workloads. Too few = underutilization; too many = scheduling overhead and small-task problem.

---

## 5-Minute Revision Cheat Sheet

- repartition: shuffle, increase or redistribute.
- coalesce: no shuffle when reducing, merge only.
- Target ~128–200MB per partition.
- coalesce before write to limit files.
