# Transaction Log and ACID

## ✅ What you need to say in interview

- **Transaction log:** Delta stores metadata as **JSON files** in `_delta_log/`. Each transaction = one or more JSON files. Log records **adds** and **removes** of data files.
- **ACID:** Atomicity, Consistency, Isolation, Durability. **Atomic:** Commit = all-or-nothing. **Consistency:** Schema + constraints. **Isolation:** Snapshot isolation. **Durability:** Log on cloud storage.
- **Optimistic concurrency:** Writers add commits; conflicts resolved at commit (e.g., concurrent appends OK; concurrent UPDATE same file = retry).

## ⚙️ How it actually works

1. Write creates new Parquet files + log entry (add file).
2. Delete/update adds log entry (remove file, add new files).
3. Reader reads log, gets list of files for version N.
4. Multiple writers: first commit wins; others detect conflict and retry.

## ✅ When to use

- Explaining why Delta supports ACID on object storage.
- Explaining time travel (log = version history).
- Explaining why small file problem exists (each write = new files until OPTIMIZE).

## ❌ When to NEVER use

- Don't say Delta uses a database—it uses a log on object storage.
- Don't confuse optimistic concurrency with locking.

## 🚩 Common interview pitfalls

- Saying the log is a single file (it's multiple JSON files, one per commit).
- Not knowing checkpoints (every 10 commits) speed up log reads.

## 💻 Working example (SQL + PySpark)

```sql
-- Create Delta table
CREATE TABLE my_table (id INT, name STRING)
USING DELTA
LOCATION '/path/to/table';
```

```python
df.write.format("delta").mode("append").save("/path/to/table")
# Creates _delta_log/00000000000000000000.json
```

## ❔ Actual interview questions + ideal answers

**Q: How does Delta Lake achieve ACID?**

- **Junior:** It uses a transaction log. Writes are atomic.
- **Senior:** Delta uses a **transaction log** (JSON files in `_delta_log/`) that records every add/remove of data files. **Atomicity:** A commit is a single log entry—all-or-nothing. **Isolation:** Readers see a **consistent snapshot** (list of files) for a version. **Durability:** Log is on cloud storage. **Optimistic concurrency** handles multiple writers—conflicts detected at commit; one wins, others retry.

**Q: What is in the Delta transaction log?**

- **Junior:** Metadata about changes.
- **Senior:** Each JSON file records **actions**: AddFile (path, size, stats), RemoveFile, metadata, protocol. Readers replay the log to get the file list for a version. **Checkpoints** (every 10 commits) persist a Parquet snapshot to avoid replaying entire log.

---

## 5-Minute Revision Cheat Sheet

- Log = JSON in _delta_log/.
- ACID via log + optimistic concurrency.
- Add/Remove file actions.
- Checkpoints every 10 commits.
