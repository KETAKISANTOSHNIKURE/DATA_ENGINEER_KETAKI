# MERGE INTO, Upserts, CDC

## ✅ What you need to say in interview

- **MERGE INTO:** **Upsert** operation—update matching rows, insert non-matching. Idempotent when key is unique.
- **Syntax:** `MERGE INTO target USING source ON condition WHEN MATCHED THEN ... WHEN NOT MATCHED THEN ...`.
- **CDC (Change Data Capture):** Ingest changes from source (insert/update/delete). MERGE handles upserts; for deletes use `WHEN MATCHED AND source._change_type = 'delete' THEN DELETE`.

## ⚙️ How it actually works

1. Join target and source on key.
2. For each match: update or delete.
3. For each non-match in source: insert.
4. Delta rewrites only affected files (file-level granularity when possible).

## ✅ When to use

- Upserts from staging/CDC.
- Idempotent pipelines (re-run safe).
- SCD Type 1 (overwrite) or Type 2 (add version columns).

## ❌ When to NEVER use

- Don't MERGE without a proper join key—risk of duplicates or incorrect updates.
- Don't use MERGE for full refresh—overwrite is faster.
- Avoid duplicate keys in source—non-deterministic updates.

## 🚩 Common interview pitfalls

- Not handling deletes in CDC (need WHEN MATCHED ... DELETE).
- Forgetting that MERGE is atomic (all-or-nothing per commit).

## 💻 Working example (SQL + PySpark)

```sql
MERGE INTO target t
USING source s ON t.id = s.id
WHEN MATCHED AND s._change_type = 'delete' THEN DELETE
WHEN MATCHED THEN UPDATE SET t.name = s.name, t.updated_at = current_timestamp()
WHEN NOT MATCHED THEN INSERT (id, name, updated_at) VALUES (s.id, s.name, current_timestamp());
```

```python
# PySpark equivalent
from delta.tables import DeltaTable
delta = DeltaTable.forPath(spark, "/path/to/target")
delta.alias("t").merge(
    source.alias("s"), "t.id = s.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

## ❔ Actual interview questions + ideal answers

**Q: How do you implement upserts in Delta?**

- **Junior:** Use MERGE INTO with WHEN MATCHED and WHEN NOT MATCHED.
- **Senior:** **MERGE INTO target USING source ON key** with **WHEN MATCHED THEN UPDATE** and **WHEN NOT MATCHED THEN INSERT**. Ensures **idempotency** when source has unique keys—re-running produces same result. For **CDC with deletes**, add `WHEN MATCHED AND source._change_type = 'delete' THEN DELETE`. Delta rewrites only affected files for efficiency.

**Q: Why use MERGE instead of overwrite for incremental loads?**

- **Junior:** MERGE only touches changed rows; overwrite replaces everything.
- **Senior:** **Overwrite** rewrites the entire table—expensive for large tables. **MERGE** only rewrites **files containing matched keys**—efficient for incremental updates. MERGE also supports **deletes** and is **idempotent**—safe to retry. Use overwrite only for full refresh of small tables.

---

## 5-Minute Revision Cheat Sheet

- MERGE = upsert; WHEN MATCHED + WHEN NOT MATCHED.
- CDC deletes: WHEN MATCHED ... DELETE.
- Idempotent with unique source key.
- Rewrites only affected files.
