# Cache and Persist

## ✅ What you need to say in interview

- **Cache:** Stores DataFrame in memory (and disk if OOM). **`cache()` = `persist(MEMORY_AND_DISK)`**.
- **Persist:** Store with chosen **storage level**—MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, etc.
- **When:** Reuse a DataFrame **multiple times** in the same application to avoid recomputation.

## ⚙️ How it actually works

1. First action on cached DataFrame: compute and store per partition.
2. Subsequent actions: read from cache (memory or disk).
3. LRU eviction if memory full (MEMORY_AND_DISK spills to disk).
4. Cache is **per-executor**; each executor caches its partitions.

## ✅ When to use

- Iterative algorithms (e.g., ML, graph).
- Multiple actions on same DataFrame.
- Reuse after expensive shuffle.

## ❌ When to NEVER use

- Don't cache if used only once—adds overhead.
- Don't cache huge datasets without enough memory—causes spilling or OOM.
- Don't forget to `unpersist()` when done to free memory.
- Don't cache before a single action and then discard.

## 🚩 Common interview pitfalls

- Saying cache persists to disk by default (cache = MEMORY_AND_DISK; MEMORY_ONLY would be pure memory).
- Caching streams (not supported; use checkpoint).
- Not unpersisting—memory leaks in long-running jobs.

## 💻 Working example (PySpark)

```python
df = spark.read.parquet("/data/").filter("year = 2024")
df.cache()  # or df.persist(StorageLevel.MEMORY_AND_DISK)

# First action — computes and caches
df.count()

# Second action — from cache
df.groupBy("region").sum("sales").show()

# When done
df.unpersist()
```

```python
from pyspark.StorageLevel import MEMORY_AND_DISK_SER  # Serialized = less memory
df.persist(MEMORY_AND_DISK_SER)
```

## ❔ Actual interview questions + ideal answers

**Q: What is the difference between cache and persist?**

- **Junior:** Cache stores in memory; persist lets you choose where.
- **Senior:** **cache()** is shorthand for **persist(MEMORY_AND_DISK)**—memory first, spill to disk on eviction. **persist()** lets you pick storage level: MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, MEMORY_AND_DISK_SER (serialized, saves memory). Use **unpersist()** when no longer needed to free resources.

**Q: When would caching hurt performance?**

- **Junior:** When the data is huge and doesn't fit in memory.
- **Senior:** (1) **Single use**—overhead of caching with no reuse. (2) **Dataset too large**—spilling to disk or OOM. (3) **Stale cache**—if upstream data changes and you expect freshness. (4) **Memory pressure**—caching pushes out other cached RDDs/DFs, causing recomputation.

---

## 5-Minute Revision Cheat Sheet

- cache() = persist(MEMORY_AND_DISK).
- Use when reusing DataFrame multiple times.
- unpersist() when done.
- Don't cache single-use or too-large datasets.
