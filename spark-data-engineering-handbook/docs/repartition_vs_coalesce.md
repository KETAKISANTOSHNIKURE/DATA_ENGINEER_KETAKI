# repartition() vs coalesce() in PySpark

## Key Difference in One Line

| | repartition() | coalesce() |
|---|---|---|
| **Partitions** | Increase OR decrease | Only DECREASE |
| **Shuffle** | Full shuffle across network | No shuffle — merges locally |
| **Speed** | Slower | Faster |
| **Distribution** | Even | May be uneven |
| **Use when** | Need more partitions / even data | Reducing partitions efficiently |

---

## repartition() — Full Shuffle

```python
# Increase partitions — full shuffle
df_repartitioned = df.repartition(200)

# Repartition by column — better for joins/groupBy
df_repartitioned = df.repartition(200, col("date"))

# Use when:
# - Data is skewed → need even distribution
# - Need to increase partition count
# - Before a large join operation
# - Writing evenly distributed output files
```

## coalesce() — No Shuffle

```python
# Decrease partitions — no shuffle, just merges
df_coalesced = df.coalesce(10)

# Use when:
# - After filtering → too many small empty partitions
# - Writing final output to fewer files
# - Reducing small files problem
# - Performance matters and even distribution not critical
```

---

## Visual Comparison

```
repartition(4):
Partition1 [A,B,C]  →  Shuffle  →  NewPart1 [A,D,G,J]
Partition2 [D,E,F]  →  Network  →  NewPart2 [B,E,H,K]
Partition3 [G,H,I]  →  Transfer →  NewPart3 [C,F,I,L]
Partition4 [J,K,L]  →           →  NewPart4 [balanced!]
Result: EVEN distribution ✅

coalesce(2):
Partition1 [A,B,C]  ─┐
Partition2 [D,E,F]  ─┴→  NewPart1 [A,B,C,D,E,F]
Partition3 [G,H,I]  ─┐
Partition4 [J,K,L]  ─┴→  NewPart2 [G,H,I,J,K,L]
Result: No shuffle, but may be uneven ⚠️
```

---

## Production Examples

### ✅ Good use of coalesce — After filtering
```python
# Start with 200 partitions
df = spark.read.parquet("s3://bucket/large_data/")
# df has 200 partitions

# Filter reduces data by 90%
df_filtered = df.filter(col("status") == "ACTIVE")
# Still 200 partitions but most are nearly empty!

# coalesce merges empty partitions efficiently
df_final = df_filtered.coalesce(20)
# Now 20 meaningful partitions ✅
df_final.write.parquet("s3://bucket/output/")
```

### ✅ Good use of repartition — Before join
```python
# Before a large join — need even distribution
df = df.repartition(200, col("customer_id"))
result = df.join(other_df, "customer_id")
# Even distribution → no skew in join ✅
```

### ❌ Wrong use of coalesce — Before join
```python
# ❌ BAD — coalesce before large join
df = df.coalesce(50)  # Uneven partitions!
result = df.join(other_df, "key")
# Skewed partitions → some executors overloaded ❌

# ✅ GOOD — repartition before join
df = df.repartition(200, col("key"))
result = df.join(other_df, "key")
```

---

## Check Partition Count

```python
# Check current partition count
print(df.rdd.getNumPartitions())

# After repartition
df_new = df.repartition(100)
print(df_new.rdd.getNumPartitions())  # 100

# After coalesce
df_new = df.coalesce(10)
print(df_new.rdd.getNumPartitions())  # 10
```

---

## Small Files Problem — Use coalesce

```python
# Problem: 10,000 small files in S3
df = spark.read.parquet("s3://bucket/raw/")
print(df.rdd.getNumPartitions())  # 10,000 partitions!

# Fix: coalesce to reasonable number
# Target: 100-200MB per file
df.coalesce(50)\
  .write\
  .mode("overwrite")\
  .parquet("s3://bucket/optimized/")
# Result: 50 files of ~100MB each ✅
```

---

## Decision Guide

```
Need to change partition count?
│
├── Increasing partitions?
│   └── Use repartition() ✅
│
├── Decreasing partitions?
│   ├── Need even distribution? (before join/groupBy)
│   │   └── Use repartition() ✅
│   └── Just reducing size? (after filter, for write)
│       └── Use coalesce() ✅ (faster, no shuffle)
│
└── Small files problem?
    └── Use coalesce() ✅
```

---

## Interview Answer

> "repartition does a full shuffle across the network and can both increase and decrease
> partitions with even distribution. coalesce only decreases partitions by merging local
> partitions without a shuffle, so it is faster but may produce uneven partitions.
> I use repartition before large joins to ensure even data distribution and prevent skew.
> I use coalesce after filtering operations where many partitions become nearly empty,
> or before writing final output to reduce small files. Using coalesce before a join was
> a mistake I learned from — it caused skew because data was not evenly distributed."
