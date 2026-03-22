# COPY INTO

## ✅ What you need to say in interview

- **COPY INTO:** **Idempotent** batch load into Delta table. **Incremental**—only copies **new or changed files** (tracks by path/size/modification time).
- **SQL:** `COPY INTO table FROM path OPTIONS (...)`. Can specify format, schema, pattern.
- **Idempotent:** Re-running skips already-loaded files. Safe for retries.
- **Use case:** Batch ingestion from cloud storage; replace full load + merge.

## ⚙️ How it actually works

1. COPY INTO lists files at path.
2. Compares with table transaction log (already copied files).
3. Copies only new/changed files.
4. Atomic per file; transaction log updated.
5. Supports pattern, format options, schema enforcement.

## ✅ When to use

- **Batch** file ingestion (scheduled, not continuous).
- **Idempotent** loads—re-run safe.
- **Incremental** by file (new files only).
- Simpler than Auto Loader when batch is sufficient.

## ❌ When to NEVER use

- Don't use for real-time streaming—use Auto Loader.
- Don't use for database CDC—use connector.
- Avoid moving/deleting source files after copy if you rely on path for idempotency (path+size+mtime used).
- Don't use COPY INTO for transformations—use for load only; transform in separate step.

## 🚩 Common interview pitfalls

- Confusing with INSERT INTO (COPY is file-based, incremental).
- COPY INTO overwrites on same path+content? No—skips. For "overwrite" behavior, use different pattern or truncate.
- Schema: COPY can infer or use provided schema.

## 💻 Working example (SQL + PySpark)

```sql
COPY INTO bronze_events
FROM 's3://bucket/landing/events/'
FILEFORMAT = PARQUET
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

-- With pattern
COPY INTO bronze_events
FROM 's3://bucket/landing/'
FILEFORMAT = JSON
PATTERN = '*.json'
```

## ❔ Actual interview questions + ideal answers

**Q: What is COPY INTO and how is it different from Auto Loader?**

- **Junior:** COPY INTO is batch load. Auto Loader is streaming.
- **Senior:** **COPY INTO** is **batch** SQL command for loading files into Delta. **Idempotent**—skips already-loaded files (by path/size/mtime). **Incremental** by file. Use for **scheduled batch** ingestion. **Auto Loader** is **streaming**—continuously monitors for new files, processes incrementally. Use Auto Loader for **continuous** arrival; COPY INTO for **batch** (e.g., daily run). Both are incremental; COPY is batch-triggered.

**Q: How does COPY INTO achieve idempotency?**

- **Junior:** It tracks what files it already copied.
- **Senior:** COPY INTO records **file path, size, modification time** in the Delta transaction log. On re-run, it **skips** files that match. Same file copied twice = skipped second time. Safe for **retries** and **overlapping runs** (e.g., same batch run twice). Source files should not be modified after copy—would be seen as "new" and re-copied.

---

## 5-Minute Revision Cheat Sheet

- COPY INTO = batch, idempotent file load.
- Tracks path/size/mtime.
- Batch-triggered; incremental by file.
- Use for scheduled ingestion.
