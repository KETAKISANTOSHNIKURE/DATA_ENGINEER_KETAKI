# Senior Mock Interview — 1 Hour

**Format:** 10 questions; ~5–6 min each. Ideal **senior-level** answers.

---

## Question 1 (5 min): Spark Architecture

**"Walk me through what happens when you run a Spark job, from submission to completion."**

### Ideal Senior Answer

"When I submit a job—say, a `count()` or `write()`—the **driver** receives the action and builds the **logical plan** from the DAG of transformations. **Catalyst** optimizes it. The driver then asks the **cluster manager** for resources and launches **executors** on workers. The **DAG Scheduler** splits the plan into **stages** at shuffle boundaries—each shuffle creates a new stage. Within a stage, **tasks** are created—one per partition. The **Task Scheduler** sends tasks to executors. Executors run tasks, perform **shuffle writes** at stage boundaries, and **shuffle reads** for the next stage. Results flow back to the driver. For a write, the driver coordinates the commit. The driver is single point of failure; executor failure triggers task retry on another executor."

---

## Question 2 (5 min): Delta Lake ACID and Transaction Log

**"How does Delta Lake achieve ACID transactions on object storage like S3?"**

### Ideal Senior Answer

"Delta uses a **transaction log**—JSON files in `_delta_log/`—that records every change as **actions**: AddFile, RemoveFile, metadata. Each **commit** is a new log file. **Atomicity**: A commit is all-or-nothing—the log entry is written atomically. **Isolation**: Readers determine which files to read by replaying the log to a version—they see a **consistent snapshot**. **Durability**: The log is on object storage; once written, it's persistent. **Optimistic concurrency**: Multiple writers can append; conflicts are detected at commit time—e.g., concurrent updates to the same file—and one retries. There are **checkpoints** every 10 commits—Parquet snapshots—to avoid replaying the full log. So we get database-like ACID without a database—just a log on S3/ADLS."

---

## Question 3 (6 min): Performance Troubleshooting

**"A job that usually runs in 10 minutes is now taking 2 hours. Same data volume. How do you debug this?"**

### Ideal Senior Answer

"First, **Spark UI**—Jobs tab to see which stage is slow. Then **Stages**—task duration distribution. If one task is 10× others, it's **skew**. I'd check if the data distribution changed—new skewed key, more nulls. Second, **shuffle read/write**—if it's huge, we may have a join or aggregation that's shuffling more data, or partition count changed. Third, **spill**—if executors are spilling, we have memory pressure; maybe partition size grew or skew is worse. Fourth, **partition count**—too many or too few can hurt. Fifth, **lineage**—did an upstream schema or filter change affect the plan? I'd run **EXPLAIN** to compare. Fixes: skew → salting or AQE; shuffle → broadcast if possible, pre-partition; spill → more memory or fewer partitions; partition count → repartition or coalesce. I'd also check if the **cluster** or **Photon** config changed."

---

## Question 4 (5 min): Medallion and Idempotency

**"Describe the Medallion architecture and explain how you ensure idempotency at each layer."**

### Ideal Senior Answer

"**Medallion** has three layers. **Bronze** is raw, immutable, append-only—we ingest exactly what arrived. Idempotency: **Auto Loader** or **COPY INTO** track processed files; re-running skips them. **Silver** is cleaned, typed, deduplicated. Idempotency: **MERGE** by unique key—same source run twice produces same result. We dedupe in the merge (e.g., window to keep latest) so we're deterministic. **Gold** is aggregated, business-ready. Idempotency: **partition overwrite**—e.g., `INSERT OVERWRITE ... PARTITION (date='x')`—or MERGE for dimension-style tables. Re-running replaces the partition with the same data. Across layers, we use **Delta ACID**—commits are atomic; a failed run leaves no partial state. We also avoid non-deterministic keys—no uuid() in business keys—so retries are truly idempotent."

---

## Question 5 (6 min): Streaming Exactly-Once

**"How do you achieve exactly-once semantics when streaming data into Delta?"**

### Ideal Senior Answer

"Exactly-once needs two things: **at-least-once delivery** and **idempotent writes**. **Checkpointing** gives at-least-once—Spark records offsets; on restart, it resumes from the last committed offset. But on failure, the same micro-batch can be **redelivered**. So the **sink** must be idempotent. For Delta, we use **foreachBatch** with **MERGE**—the merge key (e.g., primary key) ensures that processing the same batch twice produces the same result. No duplicates. We also need **transactional** semantics—Delta commits are atomic. So: checkpoint = at-least-once, MERGE = idempotent, Delta = atomic. Together, exactly-once. One nuance: if we used **append** instead of MERGE, we'd get duplicates on redelivery. And we must ensure the **source** (e.g., Kafka) and **checkpoint** are durable. For Kafka, we use the Kafka offset in the checkpoint; for file sources like Auto Loader, the checkpoint tracks files."

---

## Question 6 (5 min): Data Skew

**"You have a join where one key value has 80% of the data. How do you handle it?"**

### Ideal Senior Answer

"First, **AQE skew join**—enabled by default in Spark 3.x—can split skewed partitions at runtime. I'd try that first. If it's not enough, **salting**: add a random suffix to the key, e.g., `key_salt = key || "_" || rand(0, N)`. This spreads the hot key across N partitions. We join on key_salt, then aggregate back by original key if needed. N is a trade-off—too many = many small partitions; too few = still skewed. Sometimes we **filter** the skewed value and handle it separately—e.g., process the hot key in a dedicated path with more parallelism. Or **broadcast** the small side if the skewed key is on the large side and the 'other' side is small. I'd also check if we can **reduce** the skewed key—e.g., nulls or default values; filter those out and handle in a different way. Diagnose via Spark UI—task duration distribution—to confirm skew."

---

## Question 7 (5 min): Unity Catalog and Governance

**"How would you set up governance for a table that different teams need different access to—some read-only, some read-write, and one column must be masked for most users?"**

### Ideal Senior Answer

"For **read-only** teams: **USAGE** on catalog and schema, **SELECT** on the table. I'd use **groups**—e.g., `analytics-readonly`—and grant to the group. For **read-write** (e.g., ETL): **MODIFY** on the table. For the **masked column** (e.g., SSN): **Column-Level Security**—a mask function that returns `***` for users without a specific privilege, or we use a **view** that exposes masked data and grant SELECT on the view to analysts; grant SELECT on the base table only to authorized users. Alternatively, Delta **CLS** with a mask function. For **Row-Level Security** if needed—e.g., region-based—we'd add a filter function. I'd put this in **Unity Catalog** so it's centralized, auditable. **Audit logs** track who accessed what. **Lineage** shows downstream. I'd document the access model and review periodically."

---

## Question 8 (5 min): Pipeline Reliability

**"What does a production-ready pipeline look like in terms of reliability and observability?"**

### Ideal Senior Answer

"**Reliability**: (1) **Idempotent**—MERGE or partition overwrite so retries are safe. (2) **Retries**—task-level, 2–3 with backoff for transient failures. (3) **Alerting**—on failure (email, PagerDuty); on **SLA breach** (e.g., didn't complete by 8 AM) via a monitoring job. (4) **Secrets**—credentials in secret scopes, never in code. (5) **Environment separation**—dev/staging/prod; promote via Git. **Observability**: (1) **Metrics**—rows read/written, duration, status, written to a metrics table or pushed to Datadog. (2) **Data quality**—expectations, quarantine for bad rows, alert on quarantine spike. (3) **Lineage**—Unity Catalog for impact analysis. (4) **Runbook**—what to do when alerts fire. (5) **SLA monitoring**—compare completion time to target; alert on breach. We'd also have **backfill** and **recovery** procedures documented."

---

## Question 9 (5 min): Incremental vs Full Load

**"When would you use incremental load vs full load, and what are the trade-offs?"**

### Ideal Senior Answer

"**Incremental** when the table is large and we get **deltas**—only new or changed rows. Strategies: **timestamp** (e.g., `updated_at > last_run`), **CDC** (change stream), **file-based** (Auto Loader, COPY INTO). Benefits: less data, faster, lower cost. Risks: **late-arriving** data with timestamp; **deletes** not captured with timestamp only; complexity. **Full load** when the table is small, or we need a **complete refresh** (e.g., dimension that changes often, or source doesn't support incremental). Simpler, but expensive for large tables. **Hybrid**: full load periodically (e.g., weekly) for reconciliation; incremental daily. For **Delta**, we often do incremental with **MERGE**—idempotent. I'd choose based on source capabilities, data volume, latency requirements, and operational complexity we can support."

---

## Question 10 (6 min): End-to-End Design

**"Design a pipeline that ingests events from an S3 landing zone into a Delta lakehouse, with Bronze, Silver, and Gold layers, supporting both batch and streaming."**

### Ideal Senior Answer

"**Landing zone**: S3 path partitioned by `source/date=YYYY-MM-DD/`. Lifecycle policy to archive/delete after 30 days. **Bronze**: **Auto Loader** (streaming) or **COPY INTO** (batch) from landing. Append-only; schema-on-read; store raw JSON/Parquet. Checkpoint for streaming. **Silver**: Read from Bronze; apply schema, validate, deduplicate (window by id, keep latest). **MERGE** into Silver by primary key—idempotent. Handle bad rows via quarantine table. **Gold**: Aggregate from Silver—e.g., daily rollups by region. **Partition overwrite** by date for idempotency. **Orchestration**: Workflows—Bronze ingest (streaming or scheduled batch), Silver transform, Gold aggregate—with dependencies. **Unified batch and streaming**: Same Silver/Gold logic; Bronze can be filled by Auto Loader (streaming) or COPY (batch). Use **parameters** (date, env). **Monitoring**: Metrics (rows, duration); alert on failure and SLA. **Governance**: Unity Catalog; RLS if multi-tenant. **Optimize**: OPTIMIZE and Z-ORDER on Silver/Gold; enable optimizeWrite on Bronze."

---

## Post-Interview Self-Check

- [ ] Did you mention **specific** technologies (Delta, MERGE, Auto Loader, Unity Catalog)?
- [ ] Did you cover **trade-offs** and **when not to** use something?
- [ ] Did you tie answers to **production** experience (reliability, observability)?
- [ ] Did you structure answers (enumerate, cause→effect)?
- [ ] Did you ask a clarifying question when appropriate?

---

**Time allocation:** ~5–6 min per question. Leave 5 min for your questions at the end.
