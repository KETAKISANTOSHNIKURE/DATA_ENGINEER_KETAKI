# Auto Loader

## ✅ What you need to say in interview

- **Auto Loader:** **Incremental** file ingestion for cloud storage. Only processes **new files**; uses **checkpoint** to track processed files. Supports **schema evolution**.
- **Format:** `cloudFiles` in `readStream`. Works with S3, ADLS, GCS.
- **Options:** `cloudFiles.format` (parquet, json, etc.), `cloudFiles.schemaLocation` for evolution, `cloudFiles.inferColumnTypes`.
- **Exactly-once:** Per-file; checkpoint tracks offsets. Idempotent with Delta append.

## ⚙️ How it actually works

1. Auto Loader lists files in path; compares with checkpoint (processed files).
2. New files only are read and written to sink.
3. Checkpoint updated after successful write.
4. Schema evolution: infer from new files; merge with existing; optional schema location.

## ✅ When to use

- **Streaming** file ingestion (new files arrive continuously).
- **Landing zone** to Bronze.
- **Schema evolution** (new columns over time).
- Avoid full scan of directory.

## ❌ When to NEVER use

- Don't use for one-time batch—use COPY INTO or read.
- Don't change schema location mid-stream—breaks checkpoint.
- Avoid very high file arrival rate without tuning (backlog).
- Don't use for databases—use CDC connector.

## 🚩 Common interview pitfalls

- Confusing with COPY INTO (Auto Loader = streaming; COPY = batch).
- Schema evolution requires schema location.
- Checkpoint = per-query; new query = new checkpoint.

## 💻 Working example (SQL + PySpark)

```python
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "/path/schema")
  .option("cloudFiles.inferColumnTypes", "true")
  .load("/landing/")
  .writeStream
  .option("checkpointLocation", "/checkpoint/")
  .toTable("bronze"))
```

## ❔ Actual interview questions + ideal answers

**Q: What is Auto Loader and when do you use it?**

- **Junior:** Incremental file ingestion. Use for streaming files from cloud storage.
- **Senior:** **Auto Loader** incrementally ingests **new files** from cloud storage (S3, ADLS, GCS). Uses **checkpoint** to track processed files—no full directory scan. Use **cloudFiles** format in readStream. Supports **schema evolution** via `schemaLocation`. Use for **landing zone → Bronze** when files arrive continuously. **Exactly-once** per file. For one-time batch, use **COPY INTO** instead.

**Q: How does Auto Loader achieve exactly-once?**

- **Junior:** Checkpoint tracks what's processed.
- **Senior:** **Checkpoint** records which files have been processed. On restart, it only processes **new** files. Each file is processed **once** per checkpoint. Writing to **Delta** with append is **idempotent** per file—re-processing same file (if checkpoint lost) could duplicate; normally checkpoint is persistent. Exactly-once assumes checkpoint is durable (cloud storage).

---

## 5-Minute Revision Cheat Sheet

- Auto Loader = incremental file streaming.
- cloudFiles format; checkpoint.
- Schema evolution with schemaLocation.
- Landing zone → Bronze.
