# Incremental Load Strategies

## ✅ What you need to say in interview

- **Incremental:** Process only **new or changed** data, not full table.
- **Strategies:** (1) **Timestamp/watermark**—`WHERE updated_at > last_run`. (2) **CDC**—change data capture (insert/update/delete). (3) **Auto Loader**—file-based with checkpoint. (4) **Delta CDF**—Change Data Feed.
- **Bookmark/checkpoint:** Store last processed position; next run starts from there.

## ⚙️ How it actually works

1. Timestamp: track max(updated_at); next run filters `updated_at > max`.
2. CDC: ingest change stream; MERGE into target.
3. Auto Loader: checkpoint tracks processed files; new files only.
4. CDF: Delta provides change records; consume and MERGE.

## ✅ When to use

- Large tables, frequent runs.
- Reduce compute and time.
- Near-real-time pipelines.

## ❌ When to NEVER use

- Don't use incremental if source has no reliable change indicator.
- Don't forget to handle deletes in CDC.
- Don't use watermark without understanding late data.

## 🚩 Common interview pitfalls

- Assuming timestamp strategy works with late-arriving data.
- Not handling deletes in CDC.
- Checkpoint/watermark in non-persistent storage (lost on restart).

## 💻 Working example (SQL + PySpark)

```python
# Timestamp
last = spark.table("control_table").agg(max("last_updated")).collect()[0][0]
new_df = spark.read.parquet("/source").filter(f"updated_at > '{last}'")
# process, then update control_table

# Auto Loader
(spark.readStream.format("cloudFiles").option("cloudFiles.format", "parquet")
 .load("/landing/")
 .writeStream.option("checkpointLocation", "/checkpoint/")
 .toTable("bronze"))
```

## ❔ Actual interview questions + ideal answers

**Q: How do you implement incremental loads?**

- **Junior:** Use a watermark or last updated timestamp.
- **Senior:** Depends on source. **Timestamp:** track `max(updated_at)`; filter `WHERE updated_at > last`. Risk: late-arriving rows. **CDC:** consume change stream; MERGE by key; handle deletes. **Auto Loader:** file-based; checkpoint tracks processed files. **Delta CDF:** enable on source; read changes; MERGE. Choose based on source capabilities and latency needs.

**Q: What are the risks of timestamp-based incremental loads?**

- **Junior:** Late data can be missed.
- **Senior:** **Late-arriving data**—rows with `updated_at` in the past can be skipped. **Out-of-order commits**—source may commit older transactions after newer ones. **Deletes**—timestamp doesn't capture deletes. Mitigate: overlap window (re-process last N hours), or use CDC for full fidelity.

---

## 5-Minute Revision Cheat Sheet

- Timestamp, CDC, Auto Loader, CDF.
- Bookmark/checkpoint for position.
- Late data risk with timestamp.
- CDC needs delete handling.
