# Joins: Broadcast vs Sort-Merge

## ✅ What you need to say in interview

- **Broadcast Join:** Small table is **sent to all executors**; no shuffle on small side. Used when one table fits in executor memory.
- **Sort-Merge Join:** Both sides **shuffled** by join key, sorted, then merged. Default for large-to-large joins.
- **Broadcast threshold:** `spark.sql.autoBroadcastJoinThreshold` (default 10MB). Tables smaller than this are auto-broadcast.

## ⚙️ How it actually works

- **Broadcast:** Driver sends full small table to each executor. Each partition of large table joins locally. O(n) on large table.
- **Sort-Merge:** Hash partition both sides by join key → sort each partition → merge. O(n log n) per partition.

## ✅ When to use

- **Broadcast:** Dimension tables, lookup tables, one side << 10MB.
- **Sort-Merge:** Both sides large; broadcast would OOM.

## ❌ When to NEVER use

- Don't broadcast a large table—driver/executor OOM risk.
- Don't disable broadcast for small tables (slows joins).
- Don't use broadcast for one-to-many when the "one" side is huge.

## 🚩 Common interview pitfalls

- Saying broadcast avoids all shuffles (large table still has its partitions).
- Not knowing AQE can convert sort-merge to broadcast at runtime if stats show small side.

## 💻 Working example (PySpark)

```python
from pyspark.sql.functions import broadcast

# Force broadcast (when auto doesn't kick in)
large_df.join(broadcast(small_df), "id")

# Or set threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "50MB")
```

```sql
-- SQL: broadcast hint
SELECT /*+ BROADCAST(small_table) */ * 
FROM large_table l 
JOIN small_table s ON l.id = s.id;
```

## ❔ Actual interview questions + ideal answers

**Q: When would you use broadcast join?**

- **Junior:** When one table is small.
- **Senior:** When **one table fits in executor memory**—typically dimension/lookup tables under 10–50MB. Broadcast sends the small table to every executor so the large table can join locally without shuffle on the small side. **Force** with `broadcast()` if Catalyst doesn't auto-pick it. Don't broadcast if the "small" table is actually large—causes OOM.

**Q: What happens if both tables are 100GB? What join strategy?**

- **Junior:** Sort-merge join, maybe partition by join key.
- **Senior:** **Sort-merge join**—both sides are shuffled by join key, sorted, then merged. Broadcast is not an option. Optimization: **pre-partition** both tables by the join key to avoid shuffle; ensure **no skew** on the key; consider **salting** if skew exists.

---

## 5-Minute Revision Cheat Sheet

- Broadcast: small table → all executors, no shuffle on small side.
- Sort-merge: shuffle both, sort, merge.
- Auto-broadcast < 10MB (configurable).
- Force: `broadcast(df)` or `/*+ BROADCAST(t) */`.
