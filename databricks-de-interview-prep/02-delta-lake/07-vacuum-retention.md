# VACUUM and Retention

## ✅ What you need to say in interview

- **VACUUM:** Removes **data files** that are no longer in the current version and older than retention. Frees storage.
- **Retention:** `delta.deletedFileRetentionDuration` (default 7 days)—how long deleted files are kept before VACUUM can remove them.
- **`delta.logRetentionDuration`:** How long to keep transaction log (default 30 days)—affects **time travel**.
- **Dry run:** `VACUUM table RETAIN 168 HOURS DRY RUN` to see what would be deleted.

## ⚙️ How it actually works

1. Delta tracks which files belong to each version.
2. Files removed in a commit are "deleted" but not physically removed.
3. VACUUM deletes files that (a) are not in current version, (b) are older than retention.
4. Retention is a safety—time travel and RESTORE need those files.

## ✅ When to use

- Reclaim storage after deletes/overwrites.
- Schedule VACUUM (e.g., weekly) after retention period.
- Use DRY RUN first.

## ❌ When to NEVER use

- Don't set retention shorter than your time travel/RESTORE window.
- Don't VACUUM without retention check—default 7 days; can reduce for faster cleanup if you don't need time travel that far back.
- Don't run VACUUM too frequently—no benefit if retention hasn't passed.

## 🚩 Common interview pitfalls

- Confusing log retention with file retention.
- Not knowing VACUUM breaks time travel for versions whose files were deleted.
- Zero retention = only current version; breaks RESTORE.

## 💻 Working example (SQL + PySpark)

```sql
-- Default: 7 days retention
VACUUM my_table;

-- Custom retention (e.g., 168 hours = 7 days)
VACUUM my_table RETAIN 168 HOURS;

-- Dry run
VACUUM my_table RETAIN 168 HOURS DRY RUN;
```

```python
# Table property
ALTER TABLE my_table SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = '168 hours');
```

## ❔ Actual interview questions + ideal answers

**Q: What does VACUUM do and what are the risks?**

- **Junior:** VACUUM deletes old files. It can break time travel.
- **Senior:** **VACUUM** removes data files that are no longer referenced and older than `delta.deletedFileRetentionDuration` (default 7 days). It **frees storage**. Risk: **Time travel and RESTORE** need those files. If VACUUM removes them, you can't go back. Set retention ≥ your time travel window. Use **DRY RUN** before running.

**Q: What is the difference between logRetentionDuration and deletedFileRetentionDuration?**

- **Junior:** One is for logs, one for data files.
- **Senior:** **logRetentionDuration** (default 30 days) controls how long **transaction log** entries are kept—affects **time travel** (versions). **deletedFileRetentionDuration** (default 7 days) controls how long **deleted data files** are kept before VACUUM can remove them. Both affect recovery: log = version history; files = actual data for RESTORE.

---

## 5-Minute Revision Cheat Sheet

- VACUUM = remove old deleted files.
- deletedFileRetentionDuration = 7 days default.
- logRetentionDuration = 30 days; affects time travel.
- DRY RUN before VACUUM.
