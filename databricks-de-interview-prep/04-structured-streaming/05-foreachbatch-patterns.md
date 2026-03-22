# foreachBatch Patterns

## ✅ What you need to say in interview

- **foreachBatch:** Allows applying **batch logic** to each micro-batch. Receives `(batchDF, batchId)` and can run arbitrary code (e.g., MERGE, custom sinks).
- **Use case:** Delta MERGE, writes to JDBC, multiple sinks, custom logic that isn't natively supported.
- **Exactly-once:** Ensure logic is **idempotent** (e.g., MERGE by key); checkpoint provides at-least-once delivery of batches.

## ⚙️ How it actually works

1. Each micro-batch is passed to the foreachBatch function as a DataFrame.
2. Function runs as batch job (can use any batch API).
3. Checkpoint commits after function completes successfully.
4. Retry: same batch may be delivered again—idempotency required.

## ✅ When to use

- MERGE into Delta (streaming sink doesn't natively support MERGE).
- JDBC/API writes.
- Multiple writes from same stream.
- Custom deduplication before write.

## ❌ When to NEVER use

- Don't use non-idempotent logic—retries cause duplicates.
- Don't do heavy per-batch work that could be done incrementally.
- Avoid external side effects that aren't idempotent.

## 🚩 Common interview pitfalls

- Forgetting idempotency—MERGE is idempotent; append is not (for upserts).
- Using foreachBatch when native sink exists (e.g., toTable)—simpler.
- Not handling batchId for audit (optional).

## 💻 Working example (SQL + PySpark)

```python
def merge_batch(batch_df, batch_id):
    batch_df.createOrReplaceTempView("updates")
    batch_df.sparkSession.sql("""
      MERGE INTO target t USING updates u ON t.id = u.id
      WHEN MATCHED THEN UPDATE SET *
      WHEN NOT MATCHED THEN INSERT *
    """)

stream_df.writeStream.foreachBatch(merge_batch) \
  .option("checkpointLocation", "/checkpoint/") \
  .trigger(processingTime="10 seconds") \
  .start()
```

## ❔ Actual interview questions + ideal answers

**Q: When do you use foreachBatch?**

- **Junior:** When you need to do something the streaming sink doesn't support, like MERGE.
- **Senior:** **foreachBatch** runs **batch logic** on each micro-batch—e.g., **MERGE into Delta** (streaming doesn't support MERGE natively), **JDBC writes**, **multiple sinks**, or **custom deduplication**. The function receives `(batchDF, batchId)`. **Idempotency** is critical—on retry, the same batch may be delivered again; MERGE handles that, append does not for upserts.

**Q: How do you achieve exactly-once with foreachBatch?**

- **Junior:** Use idempotent writes like MERGE.
- **Senior:** Checkpoint gives **at-least-once** delivery of batches. For **exactly-once**, the foreachBatch logic must be **idempotent**—same batch processed twice = same result. **MERGE** by unique key is idempotent. Simple **append** is not idempotent for upserts (creates duplicates). Also ensure **transactional** sink—Delta commits are atomic.

---

## 5-Minute Revision Cheat Sheet

- foreachBatch = batch logic per micro-batch.
- Use for MERGE, JDBC, multiple sinks.
- Must be idempotent (MERGE).
- Checkpoint = at-least-once; idempotency = exactly-once.
