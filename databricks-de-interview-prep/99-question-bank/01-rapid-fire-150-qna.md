# 150 Rapid-Fire Q&A

**Format:** Question → 1–3 line answer. Drill these.

---

## Spark Core (1–25)

1. **What is the Driver?** Single JVM that plans the DAG, schedules tasks, coordinates executors, collects results.
2. **What are Executors?** JVM processes on workers that run tasks, hold cached data, perform shuffles.
3. **What is a Job?** One action (e.g., count, write) triggers one job.
4. **What is a Stage?** Set of tasks between shuffle boundaries; shuffle creates a new stage.
5. **What is a Task?** One partition processed on one executor; smallest unit of work.
6. **What is a transformation?** Returns new DataFrame; lazy; no execution until action.
7. **What is an action?** Triggers execution; returns result to driver or writes data (count, show, write, collect).
8. **What is lazy evaluation?** Spark defers execution until an action; builds optimized plan first.
9. **What is a narrow transformation?** No shuffle; output partition depends on single input partition (map, filter).
10. **What is a wide transformation?** Requires shuffle; output depends on multiple partitions (groupBy, join).
11. **What is shuffle?** Redistribution of data by key; write to disk, network, read; expensive.
12. **repartition vs coalesce?** repartition shuffles; use to increase. coalesce merges without shuffle; use to reduce.
13. **When to use coalesce?** Before write to reduce files; to decrease partitions without shuffle.
14. **When to use repartition?** Increase partitions; redistribute by key before join/groupBy.
15. **What is broadcast join?** Small table sent to all executors; no shuffle on small side.
16. **When to use broadcast join?** When one table fits in memory (typically <10–50MB).
17. **What is sort-merge join?** Both sides shuffled by key, sorted, merged; default for large joins.
18. **What is cache?** Persist with MEMORY_AND_DISK; reuse DataFrame without recompute.
19. **When to cache?** When reusing DataFrame multiple times; iterative algorithms.
20. **When NOT to cache?** Single use; dataset too large for memory.
21. **What is AQE?** Adaptive Query Execution; runtime optimizations: coalesce partitions, skew join, DPP.
22. **What is DPP?** Dynamic Partition Pruning; uses runtime filter values to skip partitions.
23. **How to debug slow Spark job?** Spark UI → Jobs → Stages → Tasks; check task duration (skew), shuffle size, spill.
24. **What does spill mean?** Data written to disk when memory full; indicates memory pressure.
25. **Why avoid collect()?** Brings all data to driver; OOM risk for large datasets.

---

## Delta Lake (26–50)

26. **What is Delta transaction log?** JSON files in _delta_log/ recording add/remove of data files; enables ACID.
27. **How does Delta achieve ACID?** Transaction log; optimistic concurrency; atomic commits.
28. **Schema enforcement vs evolution?** Enforcement rejects non-matching; evolution (mergeSchema) adds columns.
29. **How to add column to Delta table?** Use mergeSchema on write; existing rows get null for new column.
30. **What is time travel?** Query past versions: VERSION AS OF n or TIMESTAMP AS OF 'ts'.
31. **What is RESTORE?** Roll back table to previous version; creates new commit.
32. **Relationship between VACUUM and time travel?** VACUUM removes old files; time travel needs them; set retention accordingly.
33. **What does MERGE INTO do?** Upsert: update matched rows, insert non-matched; idempotent with unique key.
34. **How to handle CDC deletes in MERGE?** WHEN MATCHED AND source._change_type='delete' THEN DELETE.
35. **What does OPTIMIZE do?** Compacts small files into larger ones; improves read performance.
36. **When to run OPTIMIZE?** After append-heavy workloads; on schedule for streaming tables.
37. **What is Z-ORDER?** Colocates data by column(s); improves file pruning for filters.
38. **Z-ORDER vs partitioning?** Partition = separate directories; Z-ORDER = colocate within files. Use both.
39. **What does VACUUM do?** Removes data files no longer in current version, older than retention.
40. **Default VACUUM retention?** 7 days (deletedFileRetentionDuration).
41. **How does Delta perform DELETE?** Rewrites only files containing matching rows; uses stats for pruning.
42. **optimizeWrite table property?** Auto-coalesces small files during write.
43. **autoCompact table property?** Runs OPTIMIZE after writes when beneficial.
44. **What is a checkpoint in Delta log?** Parquet snapshot every 10 commits; speeds up log replay.
45. **Delta vs Parquet?** Delta adds transaction log, ACID, time travel, MERGE, OPTIMIZE on top of Parquet.
46. **When to use overwriteSchema?** Rare; schema migration (e.g., type change); risky.
47. **replaceWhere?** Overwrite only partitions matching predicate; efficient for partition overwrite.
48. **What is Delta CDF?** Change Data Feed; row-level changes (insert/update/delete) for downstream sync.
49. **How to read Delta CDF?** table_changes() or readStream with readChangeFeed.
50. **Delta on S3/ADLS?** Yes; transaction log on object storage; same semantics.

---

## Data Engineering Patterns (51–70)

51. **What is Medallion architecture?** Bronze (raw) → Silver (cleaned, deduped) → Gold (aggregated, marts).
52. **What is Bronze?** Raw, immutable, append-only; schema-on-read.
53. **What is Silver?** Cleaned, typed, deduplicated; single source of truth.
54. **What is Gold?** Business aggregates, dimensions, marts; consumption-ready.
55. **What is idempotency?** Same input → same output; re-run safe; no duplicates.
56. **How to make pipeline idempotent?** MERGE (upsert) or partition overwrite; Delta ACID.
57. **Incremental load strategies?** Timestamp/watermark; CDC; Auto Loader; Delta CDF.
58. **Risk of timestamp incremental?** Late-arriving data can be missed.
59. **How to deduplicate?** Window row_number() ORDER BY ts DESC, filter rn=1; then MERGE.
60. **dropDuplicates vs window dedup?** dropDuplicates arbitrary; window gives "keep latest" deterministically.
61. **How to handle late-arriving data (streaming)?** Watermark; allowedLateness; or reconciliation batch.
62. **How to handle late data (batch)?** Overlap window (re-process last N days); idempotent write.
63. **Backfill strategy?** Partition-based; overwrite partition or MERGE; idempotent; parallelize.
64. **Data quality / quarantine?** Validate; good rows → main; bad → quarantine table; alert.
65. **Why quarantine vs fail?** Good data flows; bad data isolated for fix; SLA on availability.
66. **SCD Type 1 vs 2?** Type 1 overwrite; Type 2 add version/effective dates.
67. **What is exactly-once?** Each record processed precisely once; no duplicates, no drops.
68. **How does checkpoint enable exactly-once?** Tracks offset; idempotent sink; at-least-once + idempotency = exactly-once.
69. **What is exactly-once in streaming?** Checkpoint + idempotent sink (e.g., MERGE).
70. **Idempotent key design?** No random/uuid in business key; deterministic.

---

## Structured Streaming (71–90)

71. **What is microbatch?** Process data in small batches per trigger; not record-by-record.
72. **Trigger options?** ProcessingTime (interval); Once; AvailableNow (all available then stop).
73. **What is checkpoint?** Stores offsets and metadata; enables restart and exactly-once.
74. **Why checkpoint critical?** Without it, restart reprocesses from beginning.
75. **Output modes?** Append (new rows); Update (changed rows); Complete (full result).
76. **Append + aggregation?** Requires watermark; Spark finalizes windows, emits.
77. **What is watermark?** Threshold for late data; events older than max - watermark dropped; limits state.
78. **Watermark purpose?** Limit state; enable Append for aggregations; drop late events.
79. **What is foreachBatch?** Run batch logic per micro-batch; use for MERGE, JDBC, custom sinks.
80. **foreachBatch idempotency?** Must be idempotent; retry can redeliver same batch.
81. **Streaming to Delta with MERGE?** Use foreachBatch; MERGE in function; idempotent.
82. **Auto Loader vs readStream Kafka?** Auto Loader = files; Kafka = message queue; different sources.
83. **Streaming checkpoint reuse?** Don't reuse for different query/schema; incompatible.
84. **State in streaming?** Held for aggregations/joins; purged by watermark; in checkpoint.
85. **Streaming + aggregation without watermark?** Error (unbounded state).
86. **Update mode use case?** Upserts to Delta; only changed rows written.
87. **Complete mode use case?** Small aggregation; full result each batch.
88. **Streaming CDC to Delta?** Ingest change stream; foreachBatch; MERGE with delete handling.
89. **Delta CDF for streaming?** readStream with readChangeFeed; consume changes; MERGE to target.
90. **AvailableNow vs ProcessingTime?** AvailableNow = process all, stop; ProcessingTime = continuous.

---

## Performance (91–110)

91. **How to reduce shuffle?** Broadcast small tables; pre-partition by join key; filter early.
92. **Good partition size?** ~128–200MB per partition.
93. **Partition count formula?** total_data_size / 128MB; or 2–4× cores.
94. **Small files problem?** OPTIMIZE; coalesce before write; autoOptimize.
95. **Cause of small files?** Streaming; many small appends; each write adds files.
96. **What is data skew?** Uneven partition sizes; one task does much more work.
97. **How to fix skew?** AQE skew join; salting; filter skewed keys separately.
98. **What is salting?** Add random suffix to key; spread hot keys across partitions.
99. **Partitioning strategy?** Partition by filter/join column; date for time-series; avoid high cardinality.
100. **Partition vs Z-ORDER?** Partition = directories; Z-ORDER = colocate within files.
101. **What is Photon?** Databricks vectorized engine; 3–5× faster for many queries; drop-in.
102. **How to enable Photon?** Cluster config; Photon worker nodes.
103. **Pre-partitioning for join?** Both tables partitioned by join key; avoid shuffle.
104. **Broadcast threshold default?** 10MB (spark.sql.autoBroadcastJoinThreshold).
105. **Why avoid repartition to reduce?** Use coalesce; no shuffle.
106. **Spill cause?** Executor memory full; increase memory or reduce partition size.
107. **Driver OOM causes?** collect(); broadcast huge table; accumulate results.
108. **Executor OOM causes?** Large shuffle; skew; insufficient memory.
109. **Task duration skewed?** Indicates data skew; check Spark UI.
110. **Shuffle read large?** Expensive shuffle; consider broadcast or pre-partition.

---

## Databricks Platform (111–125)

111. **All-Purpose vs Job cluster?** All-Purpose = interactive, shared; Job = ephemeral, one job, terminate.
112. **When Job cluster?** Scheduled ETL; production pipelines; cost-effective.
113. **Autoscaling?** Min-max workers; scale by pending tasks; reduces cost when idle.
114. **Cluster pools?** Pre-provisioned nodes; fast startup; attach instead of provision.
115. **dbutils.fs?** File ops: ls, cp, mv, head, mount on DBFS/cloud.
116. **dbutils.notebook.run?** Execute another notebook; pass params; get return value.
117. **dbutils.widgets?** Parameterize notebook; text, dropdown, get.
118. **dbutils.secrets.get?** Access secret by scope and key; redacted in logs.
119. **Never do with secrets?** Log or print; hardcode.
120. **Init script?** Bash at cluster start; system packages, env vars.
121. **Init script vs cluster library?** Init = system-level; library = Python/JVM packages.
122. **Cluster library vs %pip?** Cluster = all sessions; %pip = current session only.
123. **Secret scope types?** Databricks-backed; Azure Key Vault; AWS Secrets Manager.
124. **Node type: memory-optimized?** For large shuffles; OOM prevention.
125. **Photon workers?** Enable Photon acceleration on cluster.

---

## Unity Catalog (126–140)

126. **UC hierarchy?** Metastore → Catalog → Schema → Table/View/Volume.
127. **Three-level name?** catalog.schema.table.
128. **Grant read-only?** USAGE on catalog and schema; SELECT on table.
129. **MODIFY vs CREATE?** MODIFY = write, alter; CREATE = create new objects in schema.
130. **RLS?** Row-Level Security; filter rows by user/group.
131. **CLS?** Column-Level Security; mask or hide columns (PII).
132. **Lineage?** Data flow; upstream/downstream; impact analysis.
133. **Audit logs?** Who accessed what, when; compliance; export to cloud.
134. **Volume?** Directory for unstructured files in UC.
135. **UC vs Hive metastore?** UC = governance, audit, RLS/CLS; Hive = legacy.
136. **Ownership?** Owner has full control; can grant; ALTER SET OWNER.
137. **Schema evolution in UC?** Same as Delta; mergeSchema.
138. **External location?** Cloud path linked to UC; for external tables.
139. **Storage credential?** Credential to access cloud storage; used by external location.
140. **Managed vs external table?** Managed = UC controls data; external = data elsewhere, UC metadata.

---

## Orchestration, Ingestion, DevOps (141–150)

141. **Workflows?** Job = DAG of tasks; notebook, Python, SQL; dependencies; schedule.
142. **Task dependency?** Task B runs after task A; run after.
143. **Job parameters?** Pass to notebook via widgets; dbutils.widgets.get.
144. **Retry strategy?** Max retries; exponential backoff; idempotent logic.
145. **Alert on failure?** Workflows email_notifications, webhook_notifications.
146. **Airflow + Databricks?** DatabricksSubmitRunOperator; Run Submit API.
147. **Auto Loader?** Incremental file streaming; cloudFiles; checkpoint; schema evolution.
148. **COPY INTO?** Batch, idempotent file load; incremental by file.
149. **Landing zone?** Raw storage; partition by source/date; no transform; ingest to Bronze.
150. **CI/CD for Databricks?** Test on PR; deploy via Jobs API or DAB on merge; secrets for tokens.
