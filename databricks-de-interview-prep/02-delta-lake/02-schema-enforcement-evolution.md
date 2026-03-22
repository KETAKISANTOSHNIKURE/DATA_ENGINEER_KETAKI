# Schema Enforcement and Evolution

## ✅ What you need to say in interview

- **Schema enforcement:** Delta **rejects** writes that don't match the table schema (extra columns, wrong types, missing required).
- **Schema evolution:** **Allow** schema changes (add columns, change types) via `mergeSchema` or `overwriteSchema`.
- **mergeSchema:** Add new columns; existing columns must match. New columns get null for existing rows.
- **overwriteSchema:** Replace schema entirely (e.g., change column type). Use with care.

## ⚙️ How it actually works

- On write, Delta compares incoming schema with table schema.
- Enforcement: strict match required.
- Evolution: `mergeSchema` merges schemas; new columns added; `overwriteSchema` replaces.

## ✅ When to use

- **Enforcement:** Strict data quality; reject bad writes.
- **mergeSchema:** CDC, adding columns over time.
- **overwriteSchema:** Rare; schema migration (e.g., type change).

## ❌ When to NEVER use

- Don't use overwriteSchema in production without backup—loses compatibility.
- Don't assume evolution is automatic—must opt in.

## 🚩 Common interview pitfalls

- Confusing enforcement with evolution.
- Not knowing mergeSchema adds columns with nulls for old data.

## 💻 Working example (SQL + PySpark)

```python
# Schema enforcement (default) — rejects extra/missing columns
df.write.format("delta").mode("append").save("/path/")

# Schema evolution — add new columns
df.write.format("delta").mode("append").option("mergeSchema", "true").save("/path/")

# Overwrite schema (careful!)
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save("/path/")
```

```sql
-- SQL
INSERT INTO table SELECT * FROM source;  -- enforcement
-- Evolution via table property or mergeSchema option
```

## ❔ Actual interview questions + ideal answers

**Q: What is the difference between schema enforcement and evolution?**

- **Junior:** Enforcement rejects bad data; evolution allows schema changes.
- **Senior:** **Schema enforcement** (default) rejects writes that don't exactly match the table schema—wrong types, extra columns, or missing columns. **Schema evolution** via `mergeSchema` allows **adding** columns; new columns get null for existing rows. `overwriteSchema` replaces the schema entirely—use only for migrations.

**Q: How do you add a new column to a Delta table with existing data?**

- **Junior:** Use mergeSchema.
- **Senior:** Use **mergeSchema** on the next write: `option("mergeSchema", "true")`. The new column is added to the schema; existing data files don't have it—Delta returns **null** for that column when reading old files. For backfill, run an UPDATE to populate the column.

---

## 5-Minute Revision Cheat Sheet

- Enforcement: reject non-matching writes.
- mergeSchema: add columns; old rows = null.
- overwriteSchema: replace schema (risky).
