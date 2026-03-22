# Streaming CDC and Upserts

## ✅ What you need to say in interview

- **Streaming CDC:** Consume **change stream** (insert/update/delete) and apply to target. Common: Kafka with Debezium, Delta CDF, database CDC.
- **Pattern:** Ingest change events → (optionally) batch in foreachBatch → **MERGE** into Delta. Handle `_change_type` for deletes.
- **Delta CDF:** Enable `delta.enableChangeDataFeed`; read changes via `table_changes()`; stream into downstream with MERGE.

## ⚙️ How it actually works

1. Source emits changes (insert, update, delete).
2. Stream reads; optionally batch.
3. foreachBatch: MERGE with WHEN MATCHED AND delete THEN DELETE, WHEN MATCHED THEN UPDATE, WHEN NOT MATCHED THEN INSERT.
4. Idempotent with proper key.

## ✅ When to use

- Real-time sync from OLTP to lakehouse.
- Delta-to-Delta CDC.
- Kafka Debezium streams.

## ❌ When to NEVER use

- Don't forget delete handling—CDC includes deletes.
- Don't merge without proper key—duplicates or wrong updates.
- Avoid out-of-order CDC without key + version (e.g., LSN) for deterministic order.

## 🚩 Common interview pitfalls

- Only handling inserts/updates; ignoring deletes.
- Assuming order is guaranteed—use sequence/LSN for ordering.
- Not idempotent—same change delivered twice should not duplicate.

## 💻 Working example (SQL + PySpark)

```python
# Delta CDF
spark.readStream.format("delta") \
  .option("readChangeFeed", "true") \
  .option("startingVersion", 0) \
  .table("source_table") \
  .writeStream.foreachBatch(merge_cdc_batch) \
  .option("checkpointLocation", "/ckpt/") \
  .start()
```

```sql
-- Read CDF
SELECT * FROM table_changes('my_table', 0, 10);
```

## ❔ Actual interview questions + ideal answers

**Q: How do you implement streaming CDC to Delta?**

- **Junior:** Read the change stream, MERGE into Delta.
- **Senior:** Ingest the **change stream** (Kafka/Debezium, Delta CDF). Use **foreachBatch** to **MERGE** into target: **WHEN MATCHED AND _change_type='delete' THEN DELETE**, **WHEN MATCHED THEN UPDATE**, **WHEN NOT MATCHED THEN INSERT**. **Idempotent** by key. For Delta CDF, enable `delta.enableChangeDataFeed` and use `readChangeFeed` option. Order matters for out-of-order—use sequence/LSN if available.

**Q: What is Delta Change Data Feed (CDF)?**

- **Junior:** Delta can output changes—inserts, updates, deletes.
- **Senior:** **CDF** records **row-level changes** (insert, update, delete) in Delta tables. Enable with `delta.enableChangeDataFeed = true`. Read via `table_changes('table', start_version, end_version)` or `readStream` with `readChangeFeed`. Use for **downstream sync**—stream changes into another Delta table or external system. Adds storage overhead for change records.

---

## 5-Minute Revision Cheat Sheet

- CDC = change stream; MERGE with delete handling.
- foreachBatch + MERGE.
- CDF: enable on table; table_changes().
- Idempotent by key.
