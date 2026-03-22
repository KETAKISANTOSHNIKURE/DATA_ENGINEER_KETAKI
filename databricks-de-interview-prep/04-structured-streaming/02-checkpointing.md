# Checkpointing

## ✅ What you need to say in interview

- **Checkpoint:** Directory that stores **offset/progress** and **metadata** for a streaming query. Enables **restart from last processed position** and **exactly-once** semantics.
- **Contents:** Source offsets, sink commit metadata, batch IDs.
- **Critical:** Must set `checkpointLocation` for fault tolerance. Without it, restart reprocesses from beginning.

## ⚙️ How it actually works

1. After each micro-batch, Spark writes to checkpoint: source offsets, batch id, sink metadata.
2. On restart, Spark reads checkpoint, resumes from last committed offset.
3. Idempotent sink + checkpoint = exactly-once.

## ✅ When to use

- All production streaming queries.
- Required for fault tolerance and exactly-once.

## ❌ When to NEVER use

- Don't reuse checkpoint for a different query (schema/logic change)—creates new stream with new checkpoint.
- Don't put checkpoint on ephemeral storage (lost on restart).
- Don't manually modify checkpoint—corrupts state.

## 🚩 Common interview pitfalls

- Forgetting checkpoint and losing progress on failure.
- Reusing checkpoint after schema change—crashes or wrong results.
- Checkpoint on local/temp storage in cluster.

## 💻 Working example (SQL + PySpark)

```python
df.writeStream \
  .option("checkpointLocation", "/path/checkpoint/") \
  .toTable("my_table")
# Or: .start()
```

```sql
CREATE OR REPLACE TABLE my_table
AS SELECT * FROM stream(...);
-- Checkpoint auto-managed for table sink
```

## ❔ Actual interview questions + ideal answers

**Q: Why is checkpointing important in Structured Streaming?**

- **Junior:** So we can resume from where we left off after a failure.
- **Senior:** **Checkpoint** stores source **offsets** and sink **commit metadata**. On **restart**, Spark resumes from the last committed offset—no reprocessing, no duplicates. Combined with an **idempotent sink** (e.g., Delta MERGE), this gives **exactly-once** semantics. Without checkpoint, a restart would reprocess from the beginning.

**Q: What happens if you change the schema of a streaming query?**

- **Junior:** You need a new checkpoint.
- **Senior:** **Checkpoint** stores schema and logical plan. If you change the query (schema, columns, logic), the old checkpoint is **incompatible**. You must use a **new checkpoint location** (or delete the old one and accept reprocessing). For schema evolution, use `mergeSchema` on the sink and ensure the change is backward-compatible where possible.

---

## 5-Minute Revision Cheat Sheet

- Checkpoint = offset + metadata.
- Required for restart and exactly-once.
- New query/schema = new checkpoint.
- Use persistent storage (cloud).
