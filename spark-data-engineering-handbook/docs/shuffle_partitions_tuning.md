# Spark Shuffle Partitions Tuning

## What is a Shuffle?

```
Shuffle = Moving data between executors across the network

Happens during: groupBy, join, distinct, repartition, orderBy

Example:
groupBy("country") → all 'US' records must go to SAME executor
This movement across network = SHUFFLE
```

---

## What is spark.sql.shuffle.partitions?

```
Controls HOW MANY PARTITIONS are created AFTER a shuffle

Default = 200

After every groupBy/join:
→ Spark creates 200 output partitions
→ Each partition processed by one task/core
```

---

## The Problem with Default 200

```
Your Cluster: 10 executors × 4 cores = 40 cores total

Scenario A — Small Data (1GB):
200 partitions of 1GB = 5MB per partition
40 cores process 200 tasks in 5 rounds

Each task finishes in 1 second
But task scheduling overhead = 2 seconds
Overhead > Work = WASTED TIME ❌

Scenario B — Large Data (500GB):
200 partitions of 500GB = 2.5GB per partition
Each partition too big → executor runs out of memory
OOM ERROR ❌

Just Right:
Match partitions to your data size and cores
```

---

## Visual — Before vs After Fix

```
BEFORE (200 partitions, 40 cores):
Round 1: [40 tasks] ✅
Round 2: [40 tasks] ✅
Round 3: [40 tasks] ✅
Round 4: [40 tasks] ✅
Round 5: [40 tasks] ✅
= 5 ROUNDS, tiny tasks, high overhead ❌

AFTER (40 partitions, 40 cores):
Round 1: [40 tasks] ✅
= 1 ROUND, right-sized tasks ✅
```

---

## How to Set Optimal Value

```python
# Check your cluster cores
total_cores = spark.sparkContext.defaultParallelism
print(f"Total cores: {total_cores}")  # e.g. 40

# Check current setting
print(spark.conf.get("spark.sql.shuffle.partitions"))  # 200

# Set based on your data size:

# Small/Medium data (< 50GB):
spark.conf.set("spark.sql.shuffle.partitions", str(total_cores))
# e.g. "40"

# Large data (> 50GB):
spark.conf.set("spark.sql.shuffle.partitions", str(total_cores * 2))
# e.g. "80"

# Formula based on data size:
# ideal_partitions = total_data_size_mb / 128
# e.g. 5000MB / 128 = ~40 partitions
```

---

## Best Approach — Use AQE (Auto Tuning)

```python
# Let Spark figure it out automatically!
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set(
    "spark.sql.adaptive.coalescePartitions.enabled",
    "true"
)
# AQE automatically merges small shuffle partitions at runtime
# Works with Spark 3.0+
```

---

## Production Example

```python
# Before fix — job took 2 hours
spark.conf.get("spark.sql.shuffle.partitions")  # 200
df.groupBy("country_code").agg({"amount": "sum"})
# Shuffle Read: 450GB ❌ (way too much for 20GB data)

# After fix — job took 14 minutes
spark.conf.set("spark.sql.shuffle.partitions", "40")
df.groupBy("country_code").agg({"amount": "sum"})
# Shuffle Read: 18GB ✅
```

---

## Rules Summary

| Data Size | Cluster Cores | Recommended Partitions |
|---|---|---|
| < 1 GB | 40 | 40 (= cores) |
| 1–50 GB | 40 | 40–80 (1-2x cores) |
| 50–200 GB | 40 | 80–160 (2-4x cores) |
| 200 GB+ | 40 | Data/128MB formula |

---

## Each Partition Should Be 100–200MB

```python
# Calculate ideal partitions
data_size_mb = 5000  # 5GB in MB
target_partition_size_mb = 128

ideal_partitions = data_size_mb / target_partition_size_mb
print(f"Ideal partitions: {ideal_partitions}")  # ~40

spark.conf.set("spark.sql.shuffle.partitions", str(int(ideal_partitions)))
```

---

## Interview Answer

> "By default Spark creates 200 shuffle partitions after every groupBy or join.
> If my cluster has only 40 cores and data is small, 200 tiny partitions means more
> scheduling overhead than actual work. I set shuffle partitions to match total cluster
> cores — 40 in our case — so all cores process exactly 40 partitions in one round.
> This reduced a job from 2 hours to 14 minutes. For large datasets I keep it higher —
> around Data Size divided by 128MB — to avoid partitions becoming too large and causing OOM.
> The best approach is enabling AQE which auto-tunes partition count at runtime."
