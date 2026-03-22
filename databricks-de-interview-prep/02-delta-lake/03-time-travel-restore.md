# Time Travel and RESTORE

## ✅ What you need to say in interview

- **Time travel:** Query **past versions** of a Delta table by version number or timestamp.
- **Syntax:** `VERSION AS OF n` or `TIMESTAMP AS OF 'timestamp'`.
- **RESTORE:** Roll back table to a previous version. Creates a new version; doesn't delete history.
- **Retention:** Default 30 days for time travel. Configurable via `delta.logRetentionDuration`.

## ⚙️ How it actually works

- Transaction log keeps history of file add/remove per version.
- Time travel: reader uses log to get file list for version N.
- RESTORE: add a new commit that "removes" current files and "adds" files from old version.

## ✅ When to use

- **Time travel:** Audit, debug "what did data look like?", compare versions.
- **RESTORE:** Rollback bad writes, undo mistaken deletes.

## ❌ When to NEVER use

- Don't RESTORE if VACUUM has removed old files—RESTORE needs those files.
- Don't assume infinite retention—default 30 days.

## 🚩 Common interview pitfalls

- Confusing time travel (read-only) with RESTORE (rollback).
- Not knowing retention limits time travel.
- VACUUM can break time travel for older versions.

## 💻 Working example (SQL + PySpark)

```sql
-- Time travel by version
SELECT * FROM my_table VERSION AS OF 5;

-- Time travel by timestamp
SELECT * FROM my_table TIMESTAMP AS OF '2024-01-15 10:00:00';

-- RESTORE to version
RESTORE TABLE my_table TO VERSION AS OF 5;

-- RESTORE to timestamp
RESTORE TABLE my_table TO TIMESTAMP AS OF '2024-01-15 10:00:00';
```

```python
# PySpark
spark.read.format("delta").option("versionAsOf", 5).load("/path/")
spark.read.format("delta").option("timestampAsOf", "2024-01-15").load("/path/")
```

## ❔ Actual interview questions + ideal answers

**Q: How do you roll back a Delta table after a bad write?**

- **Junior:** Use RESTORE to a previous version.
- **Senior:** Use **RESTORE TABLE table TO VERSION AS OF n** (or TIMESTAMP). This creates a new commit that rolls the table back—it doesn't delete history. **Prerequisite:** The files for that version must still exist. If **VACUUM** has run and removed them (default 7-day retention), RESTORE fails. Ensure `delta.deletedFileRetentionDuration` is long enough.

**Q: What is the relationship between VACUUM and time travel?**

- **Junior:** VACUUM deletes old files; that can break time travel.
- **Senior:** **VACUUM** removes data files no longer in the latest version (and beyond retention). **Time travel** needs those old files to read past versions. If VACUUM deletes them, time travel to those versions **fails**. Default retention is 7 days for deleted files. Keep `delta.deletedFileRetentionDuration` ≥ your time-travel window.

---

## 5-Minute Revision Cheat Sheet

- VERSION AS OF n, TIMESTAMP AS OF 'ts'.
- RESTORE creates new version; needs old files.
- VACUUM can break time travel.
- logRetentionDuration = time travel window.
