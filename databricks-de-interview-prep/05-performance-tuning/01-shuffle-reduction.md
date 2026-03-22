# Shuffle Reduction

## ✅ What you need to say in interview

- **Shuffle is expensive:** Disk write, network transfer, deserialization. **Minimize** it.
- **Techniques:** (1) **Broadcast** small tables. (2) **Pre-partition** by join/group key. (3) **Reduce data before shuffle** (filter, project early). (4) **Avoid unnecessary repartition**. (5) **AQE** coalesces partitions, handles skew.
- **Increase broadcast threshold** if appropriate (`spark.sql.autoBroadcastJoinThreshold`).

## ⚙️ How it actually works

- Shuffle: data repartitioned by key; written to disk, sent over network.
- Broadcast: small table replicated to all executors; no shuffle on that side.
- Pre-partitioning: both sides already partitioned by key; no shuffle (or minimal).

## ✅ When to use

- Always consider shuffle for join/groupBy.
- Broadcast for dimension tables.
- Pre-partition when both tables share same partition key.

## ❌ When to NEVER use

- Don't broadcast large tables—OOM.
- Don't repartition before narrow operations unnecessarily.
- Don't shuffle when a broadcast would work.

## 🚩 Common interview pitfalls

- Not knowing AQE can reduce shuffle (coalesce partitions).
- Over-shuffling: multiple repartitions in a pipeline.
- Filtering after join instead of before.

## 💻 Working example (SQL + PySpark)

```python
# Broadcast
df1.join(broadcast(small_df), "id")

# Pre-partition before join
df1.repartition("key").join(df2.repartition("key"), "key")

# Filter early
df.filter("date = '2024-01-01'").join(...)  # reduce before join
```

## ❔ Actual interview questions + ideal answers

**Q: How do you reduce shuffle in Spark?**

- **Junior:** Use broadcast for small tables; filter early.
- **Senior:** (1) **Broadcast** small tables—eliminates shuffle on that side. (2) **Pre-partition** both sides by join key so data is already colocated. (3) **Filter and project early**—reduce data before shuffle. (4) **Avoid repartition** before narrow ops. (5) **AQE** coalesces partitions post-shuffle. (6) Increase **broadcast threshold** if small tables are slightly over default.

**Q: When does pre-partitioning help joins?**

- **Junior:** When both tables are partitioned by the same key.
- **Senior:** When **both** tables are **partitioned by the join key** (e.g., both by `region`), Spark can **avoid shuffle**—each partition joins with the matching partition. Requires that both were written with same partition key. Useful for large-to-large joins where broadcast isn't possible.

---

## 5-Minute Revision Cheat Sheet

- Broadcast, pre-partition, filter early.
- AQE coalesce.
- Don't over-shuffle.
