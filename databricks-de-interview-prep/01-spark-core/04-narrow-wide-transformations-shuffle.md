# Narrow vs Wide Transformations, Shuffle

## ✅ What you need to say in interview

- **Narrow:** Each partition's output goes to **at most one partition** of the child. **No shuffle.** Examples: `map`, `filter`, `select`, `mapPartitions`.
- **Wide:** Output of one partition can go to **multiple partitions** of the child. **Requires shuffle.** Examples: `groupBy`, `join`, `distinct`, `repartition`.
- **Shuffle:** **Redistribution of data** across executors—data written to disk, sent over network, read by other executors.

## ⚙️ How it actually works

- Narrow: Each task reads its partition, writes to same "logical" partition. No network.
- Wide: Data must be repartitioned by key. Spark writes shuffle files; next stage reads them. **Expensive** (disk I/O, network, serialization).

## ✅ When to use

- Explaining why `groupBy` is slower than `filter`.
- Justifying broadcast joins (avoid shuffle on small table).
- Debugging slow stages (look for shuffle read/write).

## ❌ When to NEVER use

- Don't add unnecessary shuffles (e.g., `repartition` before a narrow op that doesn't need it).
- Don't say "narrow = fast, wide = slow" as a blanket rule—wide is necessary for aggregations.

## 🚩 Common interview pitfalls

- Calling `distinct` a narrow transformation (it's wide—requires shuffle).
- Not knowing `coalesce` is narrow.

## 💻 Working example (PySpark)

```python
# Narrow — no shuffle
df.filter("amount > 0").select("id", "amount")  # Each partition stays independent

# Wide — shuffle
df.groupBy("region").sum("sales")   # Shuffle by region
df1.join(df2, "id")                 # Shuffle both sides by join key (unless broadcast)
```

## ❔ Actual interview questions + ideal answers

**Q: What is shuffle and why is it expensive?**

- **Junior:** Shuffle moves data between nodes. It's slow because of network.
- **Senior:** **Shuffle** redistributes data by key for operations like `groupBy` and `join`. It's expensive because: (1) **Shuffle write**—data serialized and written to local disk, (2) **Network transfer**—other executors fetch data, (3) **Shuffle read**—deserialization. Minimizing shuffle is a key optimization.

**Q: Is `coalesce` narrow or wide?**

- **Junior:** Narrow, because it reduces partitions without shuffle.
- **Senior:** **Narrow.** `coalesce` combines partitions within the same executor when possible—no data movement across the network. `repartition` is **wide**—it always shuffles.

---

## 5-Minute Revision Cheat Sheet

- Narrow: map, filter, select — no shuffle.
- Wide: groupBy, join, distinct, repartition — shuffle.
- Shuffle = write to disk → network → read.
- Minimize shuffle; use broadcast for small joins.
