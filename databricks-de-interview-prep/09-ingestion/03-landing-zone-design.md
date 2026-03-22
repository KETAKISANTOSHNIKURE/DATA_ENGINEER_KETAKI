# Landing Zone Design

## ✅ What you need to say in interview

- **Landing zone:** **Raw** storage area where data first arrives. Before Bronze. **Immutable**; append-only.
- **Design:** Partition by **source**, **date** (e.g., `source=orders/date=2024-01-15/`). **Lifecycle policies** (archive/delete old data). **Format** per source (JSON, CSV, Parquet).
- **Pattern:** External systems write to landing → Auto Loader or COPY INTO → Bronze. **Don't transform** in landing.
- **Multi-tenant:** Separate paths per source/tenant for isolation and access control.

## ⚙️ How it actually works

1. Data producers (apps, ETL tools) write to landing path (S3, ADLS).
2. Databricks ingests from landing to Bronze (Delta).
3. Landing can be retained for audit, reprocessing; lifecycle policy cleans up.
4. Partitioning aids listing and incremental reads.

## ✅ When to use

- All batch/streaming ingestion from files.
- Multi-source pipelines.
- Need raw copy for audit or replay.

## ❌ When to NEVER use

- Don't run queries directly on landing for production—use Bronze.
- Don't transform in landing—keep raw.
- Avoid flat structure for large scale—partition.
- Don't skip lifecycle—cost grows unbounded.

## 🚩 Common interview pitfalls

- Landing vs Bronze—landing = raw; Bronze = first Delta layer.
- Not having retention/lifecycle—storage cost.
- Over-partitioning (e.g., by hour when daily is enough).

## 💻 Working example (SQL + PySpark)

```
# Landing zone structure
/mnt/landing/
  orders/
    date=2024-01-15/
      part-00001.json
      part-00002.json
  events/
    date=2024-01-15/
      *.parquet

# Lifecycle: delete after 30 days (S3/ADLS policy)
# Ingestion: Auto Loader from /mnt/landing/orders/
```

## ❔ Actual interview questions + ideal answers

**Q: How do you design a landing zone for data ingestion?**

- **Junior:** Raw storage, partition by date and source. Don't transform.
- **Senior:** **Landing zone** is **raw** storage—append-only, **immutable**. Partition by **source** and **date** (e.g., `source/date=YYYY-MM-DD/`). Use **lifecycle policies** to archive/delete after retention. **No transformation**—keep raw for audit and replay. Ingest to Bronze via **Auto Loader** (streaming) or **COPY INTO** (batch). Multi-tenant: separate paths. Format per source capability (JSON, Parquet).

**Q: Why separate landing zone from Bronze?**

- **Junior:** Landing is raw; Bronze is first processed layer.
- **Senior:** **Landing** is **raw**—exactly what arrived. **Bronze** is **first Delta** layer—typed, possibly deduped. Separation allows: (1) **Reprocessing** from raw without re-fetching from source. (2) **Audit**—raw preserved. (3) **Schema evolution** in Bronze without touching landing. (4) **Access control**—landing may be restricted; Bronze is for pipelines.

---

## 5-Minute Revision Cheat Sheet

- Landing = raw, immutable.
- Partition by source, date.
- Lifecycle for retention.
- No transform; ingest to Bronze.
