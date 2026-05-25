# Spark UI Debugging — Production Examples

## What is Spark UI?

Spark UI is a web interface showing everything happening inside your Spark job —
stages, tasks, executors, memory, shuffle, and errors.

```
Access:
Local      → http://localhost:4040
Databricks → Cluster → Spark UI button
YARN       → http://<driver-node>:4040
```

---

## Spark UI Tabs Overview

```
Spark UI
├── Jobs      → All jobs, status, duration
├── Stages    → Each stage and tasks inside
├── Tasks     → Individual task details
├── Storage   → Cached DataFrames
├── Executors → Memory, cores, GC time
├── SQL       → Query plans, DAG visualization
└── Environment → Spark configs
```

---

## Production Example 1 — OOM Error (Data Skew)

### Scenario
> Daily migration job at 1 AM failed with OutOfMemoryError.
> 50 million records from Teradata being processed in Databricks.

### Step 1 — Jobs Tab
```
Job 0 → FAILED ❌
  Duration: 45 mins (normally 20 mins)
  Failed Stage: Stage 3 (Join operation)
```

### Step 2 — Stages Tab
```
Stage 3 Details:
Total Tasks: 200
Completed:    45  ✅
Failed:        1  ❌
Killed:      154  ⬜

Failed Task 67:
Duration: 38 mins (others took 2 mins!) ← SKEW SIGNAL
```

### Step 3 — Tasks Tab
```
Task 67  → 38 mins → 45 million records ❌ SKEWED!
Task 23  → 2 mins  → 250,000 records
Task 45  → 2 mins  → 230,000 records
```

### Step 4 — Executors Tab
```
Executor 3:
├── GC Time: 85%  ❌ (should be < 10%)
├── Memory Used: 19.8GB / 20GB ❌
└── Tasks Failed: 3

Other Executors:
├── GC Time: 2-5% ✅
└── Memory Used: 2-4GB ✅
```

### Step 5 — SQL Tab (Root Cause)
```
SortMergeJoin on country_code:
country_code = 'US' → 45M records (90% of data!)
country_code = 'UK' → 2M records
country_code = 'IN' → 1M records

Root Cause: Join key severely skewed on 'US'
```

### Fix

```python
# ❌ Original — caused skew
result = large_df.join(lookup_df, "country_code")

# ✅ Fix 1 — Broadcast Join (lookup is small)
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(lookup_df), "country_code")

# ✅ Fix 2 — Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# ✅ Fix 3 — Salting for severe skew
import random
from pyspark.sql.functions import concat, lit, floor, explode, array

SALT = 10
large_df = large_df.withColumn(
    "salted_key",
    concat(col("country_code"), lit("_"),
           (floor(random.random() * SALT)).cast("string"))
)
lookup_df = lookup_df.withColumn(
    "salt_array", array([lit(i) for i in range(SALT)])
).withColumn("salt", explode(col("salt_array"))) \
 .withColumn("salted_key",
    concat(col("country_code"), lit("_"), col("salt").cast("string")))

result = large_df.join(lookup_df, "salted_key")
```

### Result
```
Before: FAILED at 45 mins, GC 85%, OOM
After:  Completed in 12 mins, GC 3-5% ✅
```

---

## Production Example 2 — Slow Job (Shuffle Problem)

### Scenario
> groupBy job suddenly went from 15 minutes to 2 hours.

### Spark UI Finding — Stages Tab
```
Shuffle Read Size:  450 GB ❌ (normally 20GB!)
Input:               50 GB
Shuffle:            450 GB ← 9x bigger than input!
```

### Root Cause
```
Default shuffle partitions = 200
Cluster cores = 40 (10 executors × 4 cores)
200 partitions / 40 cores = 5 rounds
But each partition is tiny → huge scheduling overhead
```

### Fix
```python
# Check current setting
print(spark.conf.get("spark.sql.shuffle.partitions"))  # 200

# Fix — match cluster cores
spark.conf.set("spark.sql.shuffle.partitions", "40")

# OR use AQE to auto-tune
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

### Result
```
Before: 2 hours, 450GB shuffle, 200 tiny partitions
After:  14 mins, 18GB shuffle ✅
```

---

## Production Example 3 — Small Files Problem

### Scenario
> Writing output to S3 taking 45 minutes even though processing finished in 5 minutes.

### Spark UI Finding — Stages Tab
```
Stage 4 (Write to S3):
Tasks: 10,000 ❌
Each task writing: 500KB
Total files: 10,000 small files!
```

### Fix
```python
# ❌ Problem
df.write.parquet("s3://bucket/output/")
# Creates 10,000 files of 500KB each!

# ✅ Fix — coalesce before writing
df.coalesce(50)\
  .write\
  .parquet("s3://bucket/output/")
# Creates 50 files of ~100MB each ✅
```

### Result
```
Before: 10,000 files, 45 min write
After:  50 files, 3 min write ✅
```

---

## Debugging Checklist

```
Job Failed? Follow this order:

1. Jobs Tab
   └── Which job failed? What stage?

2. Stages Tab
   └── Which stage is slow/failed?
   └── Check shuffle read/write size
   └── Check input/output records

3. Tasks Tab
   └── Any task much longer than others? → SKEW
   └── Any task failing repeatedly? → OOM or bad data

4. Executors Tab
   └── GC time > 10%? → Memory issue
   └── Any executor dead? → Node crashed

5. SQL Tab
   └── Check query plan
   └── SortMergeJoin → consider broadcast
   └── Exchange → shuffle happening

6. Environment Tab
   └── Check configs
   └── Verify memory settings
```

---

## Key Metrics to Watch

| Metric | Healthy | Problem |
|---|---|---|
| GC Time | < 10% | > 10% → memory issue |
| Task Duration | Similar across tasks | One much longer → skew |
| Shuffle Size | Small | Very large → investigate |
| Failed Tasks | 0 | Any → check logs |
| Executor Memory | < 80% used | > 90% → OOM risk |
| Input vs Shuffle | Shuffle < 3x input | Shuffle > 5x → investigate |

---

## How to Fix OOM Errors — Summary

```python
# 1. Increase executor memory
spark.conf.set("spark.executor.memory", "8g")

# 2. Fix data skew — broadcast small tables
result = large_df.join(broadcast(small_df), "key")

# 3. Repartition skewed data
df = df.repartition(200, col("skewed_column"))

# 4. Avoid collect() on large data
# ❌ all_data = df.collect()
# ✅ sample = df.take(100)

# 5. Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

---

## Interview Answer

> "When a production job fails I go to Spark UI and follow a systematic approach.
> Jobs tab to find which stage failed. Stages tab for shuffle sizes. Tasks tab to check
> if one task takes much longer — that means data skew. Executors tab to check GC time —
> above 10% means memory pressure. SQL tab for query plan to spot bad joins.
> In one real case our 1 AM job failed with OOM — Spark UI showed Task 67 had 45M records
> vs 200K in others. Root cause was skew on country_code join key. Fixed with broadcast
> join and AQE. Job went from failing at 45 mins to completing in 12 mins."
