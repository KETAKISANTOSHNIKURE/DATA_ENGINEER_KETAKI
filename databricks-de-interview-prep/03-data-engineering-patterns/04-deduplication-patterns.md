# Deduplication Patterns

## ✅ What you need to say in interview

- **Dedup:** Ensure **one row per business key** (or per key + version).
- **Patterns:** (1) **Window + MERGE**—rank by timestamp, keep latest. (2) **dropDuplicates**—within batch. (3) **MERGE**—natural dedup when key is unique.
- **Deterministic ordering:** For "latest" dedup, use deterministic sort (e.g., `updated_at`, `id`) so results are reproducible.

## ⚙️ How it actually works

1. Window: `row_number() OVER (PARTITION BY key ORDER BY ts DESC)`; filter `rn = 1`.
2. MERGE: source has dupes; use subquery with dedup. Target gets one row per key.
3. dropDuplicates: Spark drops duplicates within DataFrame; order can be non-deterministic unless specified.

## ✅ When to use

- Bronze→Silver when source can have duplicates.
- CDC with multiple changes per key (keep latest).
- Idempotent upserts.

## ❌ When to NEVER use

- Don't dropDuplicates without specifying columns—behavior can be undefined.
- Don't dedupe on non-deterministic order (e.g., without ORDER BY).
- Avoid deduping before necessary—push to Silver.

## 🚩 Common interview pitfalls

- dropDuplicates keeps "first" or "arbitrary" row—may not be "latest."
- Not deduping in streaming before merge—can cause duplicates.
- Dedup scope: per-batch vs global (streaming).

## 💻 Working example (SQL + PySpark)

```sql
-- Dedup with window, then MERGE
WITH deduped AS (
  SELECT *, row_number() OVER (PARTITION BY id ORDER BY updated_at DESC) as rn
  FROM bronze_staging
)
MERGE INTO silver t USING (SELECT * FROM deduped WHERE rn = 1) s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

```python
# PySpark
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
w = Window.partitionBy("id").orderBy(col("updated_at").desc())
df_dedup = df.withColumn("rn", row_number().over(w)).filter("rn = 1").drop("rn")
```

## ❔ Actual interview questions + ideal answers

**Q: How do you deduplicate in a Delta pipeline?**

- **Junior:** Use dropDuplicates or a window to keep the latest.
- **Senior:** For **batch:** use **window** `row_number() OVER (PARTITION BY key ORDER BY updated_at DESC)` and filter `rn = 1`, then **MERGE** into target. For **streaming:** dedupe within each micro-batch (or use foreachBatch with dedup) before merge. **dropDuplicates** works within a batch but doesn't guarantee "latest"—specify `orderBy` in a window for deterministic "keep latest." MERGE with unique key is idempotent—handles re-runs.

**Q: Why use window + MERGE instead of just dropDuplicates?**

- **Junior:** To keep the latest record.
- **Senior:** **dropDuplicates** keeps one row per key but doesn't guarantee which one—often arbitrary. For **"keep latest"** semantics, use **window + row_number()** with explicit `ORDER BY updated_at DESC` so the choice is deterministic. Then MERGE ensures idempotency when writing to Delta.

---

## 5-Minute Revision Cheat Sheet

- Window row_number for "keep latest."
- MERGE for idempotent upsert.
- dropDuplicates: within batch, order not guaranteed.
- Streaming: dedup per micro-batch before merge.
