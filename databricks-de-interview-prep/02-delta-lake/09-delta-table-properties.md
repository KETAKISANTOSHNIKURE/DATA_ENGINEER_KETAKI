# Delta Table Properties

## ✅ What you need to say in interview

- **Table properties:** Key-value config for Delta tables. Set via `ALTER TABLE ... SET TBLPROPERTIES` or at create time.
- **Key properties:** `delta.deletedFileRetentionDuration`, `delta.logRetentionDuration`, `delta.autoOptimize.optimizeWrite`, `delta.autoOptimize.autoCompact`.
- **delta.autoOptimize.optimizeWrite:** Auto-coalesce small files on write (target ~128MB).
- **delta.autoOptimize.autoCompact:** Run OPTIMIZE after writes when beneficial.

## ⚙️ How it actually works

- Properties stored in table metadata.
- Optimize write: batches small outputs before write.
- Auto compact: triggers OPTIMIZE when too many small files.

## ✅ When to use

- **optimizeWrite:** Streaming, small-batch appends.
- **autoCompact:** Append-heavy, avoid manual OPTIMIZE schedule.
- **Retention:** Tune for time travel vs storage.

## ❌ When to NEVER use

- Don't enable autoCompact on tables with frequent overwrites—overhead.
- Don't set retention too low if you need time travel.

## 🚩 Common interview pitfalls

- Confusing optimizeWrite (write path) with OPTIMIZE (read path compaction).
- Not knowing property names by heart.

## 💻 Working example (SQL + PySpark)

```sql
-- Create with properties
CREATE TABLE my_table (id INT, name STRING)
USING DELTA
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true',
  'delta.deletedFileRetentionDuration' = '168 hours'
);

-- Alter
ALTER TABLE my_table SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true');
```

## ❔ Actual interview questions + ideal answers

**Q: What is delta.autoOptimize.optimizeWrite?**

- **Junior:** It helps with small files on write.
- **Senior:** **optimizeWrite** automatically **coalesces small files** during writes—batches output to ~128MB per file. Reduces small-file problem for **streaming and append** workloads without manual OPTIMIZE. **autoCompact** runs OPTIMIZE after writes when needed. Both are table-level; enable for append-heavy tables.

**Q: How do you tune Delta retention for a table that needs 14-day time travel?**

- **Junior:** Set log retention to 14 days.
- **Senior:** Set **delta.logRetentionDuration** ≥ 14 days for time travel. Set **delta.deletedFileRetentionDuration** ≥ 14 days so **VACUUM** doesn't remove files needed for RESTORE. Example: `'delta.logRetentionDuration' = '14 days'`, `'delta.deletedFileRetentionDuration' = '14 days'`.

---

## 5-Minute Revision Cheat Sheet

- optimizeWrite: coalesce on write.
- autoCompact: OPTIMIZE after writes.
- logRetention: time travel.
- deletedFileRetention: VACUUM / RESTORE.
