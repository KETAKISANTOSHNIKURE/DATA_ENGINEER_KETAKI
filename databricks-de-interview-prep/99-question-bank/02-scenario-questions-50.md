# 50 Scenario Questions

**Format:** Problem → Good Answer → Great Answer → Common Mistakes

---

## 1. Job running 10× slower than yesterday

**Problem:** Same dataset, same code; job takes 10× longer today.

**Good:** Check Spark UI for skew, shuffle size, spill. Compare partition count. Look for more data or different distribution.

**Great:** Compare **task duration distribution**—if one task 10× others, it's skew (e.g., new skewed key). Check **shuffle read/write**—large increase? **Spill**—memory pressure? **Partition count**—too many/few? **Data volume**—has it grown? Check **lineage**—upstream schema or filter change? Run **EXPLAIN** to compare plans.

**Mistakes:** Blaming cluster size only; not checking data distribution; ignoring upstream changes.

---

## 2. Streaming job creating thousands of small files

**Problem:** Delta table has 50K small files; queries slow.

**Good:** Run OPTIMIZE. Use coalesce before write. Enable autoOptimize.optimizeWrite.

**Great:** **Immediate:** OPTIMIZE table. **Long-term:** (1) Enable `delta.autoOptimize.optimizeWrite` to coalesce on write. (2) Use `coalesce(N)` in foreachBatch before write. (3) Schedule **OPTIMIZE** (e.g., nightly). (4) If partitioned, `OPTIMIZE ... WHERE partition = value` incrementally. Target ~128MB per file.

**Mistakes:** OPTIMIZE once and forgetting; not enabling optimizeWrite for new data.

---

## 3. MERGE taking hours on 100M row table

**Problem:** MERGE into large table is very slow.

**Good:** Partition by join key. Z-ORDER by join key. Increase resources. Check skew.

**Great:** (1) **Partition** target by join key if not already. (2) **Z-ORDER** by join key for file pruning. (3) **Pre-partition source** by same key to reduce shuffle. (4) **Batch** source (e.g., foreachBatch in streaming) if from stream. (5) **Skew**—check task distribution; salt or AQE. (6) **OPTIMIZE** before MERGE if many small files. (7) **Photon** if on Databricks.

**Mistakes:** MERGE without partitioning; not batching; ignoring file count.

---

## 4. OOM on executor during join

**Problem:** Executor runs out of memory during large join.

**Good:** Increase executor memory. Check if broadcast is possible. Reduce partition size. Check skew.

**Great:** (1) **Broadcast** small table if fits in memory. (2) **Increase** executor memory. (3) **Repartition** to more, smaller partitions. (4) **Skew**—one partition too large; salting or AQE skew join. (5) **Spill**—ensure enough disk. (6) **Filter early** to reduce data before join. (7) **Pre-partition** both sides by join key to avoid shuffle explosion.

**Mistakes:** Only increasing memory; not checking skew; broadcasting too-large table.

---

## 5. Pipeline creates duplicates on retry

**Problem:** Job fails; retry creates duplicate rows in target.

**Good:** Use MERGE instead of append. Make pipeline idempotent. Use unique key.

**Great:** **Root cause:** Append without deduplication is not idempotent. **Fix:** (1) **MERGE** into target with unique key (e.g., id). (2) **Partition overwrite** if batch by partition—replace partition on re-run. (3) Ensure **source** has unique key; dedupe before merge if needed. (4) **Deterministic** keys—no uuid() in key. (5) **Checkpoint** in streaming—ensures at-least-once; idempotent sink = exactly-once.

**Mistakes:** Append for upserts; non-deterministic keys; no unique key in MERGE.

---

## 6. Need to backfill 2 years of data

**Problem:** New pipeline; need to load 2 years historically.

**Good:** Process by partition (e.g., date). Run in parallel. Use idempotent writes.

**Great:** (1) **Partition-based** backfill—iterate dates. (2) **Idempotent**—overwrite partition or MERGE. (3) **Parallelize**—workflow with multiple tasks (e.g., 12 tasks, each 2 months). (4) **Checkpoint**—track completed partitions; resume on failure. (5) **Resource**—ensure cluster can handle; consider splitting by more partitions. (6) **Validate**—compare row counts to source for sample partitions.

**Mistakes:** Full table overwrite; no parallelism; no resume strategy; not idempotent.

---

## 7. Late-arriving data in batch pipeline

**Problem:** Some rows have updated_at in the past; incremental load misses them.

**Good:** Use overlap window—re-process last N days. Or use CDC instead of timestamp.

**Great:** (1) **Overlap window:** Each run processes `[last_run - N days, now]`; N = max expected lateness. (2) **Idempotent** writes (MERGE or partition overwrite) so re-processing is safe. (3) **CDC** from source if available—captures all changes. (4) **Reconciliation job:** Periodic full or sample check for late keys; merge them. (5) **Document** SLA—e.g., "data with updated_at within 7 days" to set expectations.

**Mistakes:** Strict watermark only; no overlap; no reconciliation path.

---

## 8. Streaming job fails with "Checkpoint incompatible"

**Problem:** Changed query/schema; stream fails on restart.

**Good:** Use new checkpoint location. Or fix schema to be compatible.

**Great:** **Cause:** Checkpoint stores logical plan and schema; change breaks compatibility. **Fix:** (1) **New checkpoint**—use new path; stream restarts (reprocesses from source if needed). (2) **Schema evolution:** Use mergeSchema on sink; ensure change is additive (new columns). (3) **Migration:** Stop stream; update schema; start with new checkpoint. Document that checkpoint is tied to query.

**Mistakes:** Deleting checkpoint hoping to "reset"; reusing checkpoint for different query.

---

## 9. Need to roll back Delta table after bad write

**Problem:** Mistaken overwrite; need to restore previous state.

**Good:** Use RESTORE TABLE TO VERSION AS OF n. Or time travel to query old data.

**Great:** (1) **RESTORE** to version: `RESTORE TABLE t TO VERSION AS OF n` (or TIMESTAMP). (2) **Prerequisite:** Files for that version must exist—VACUUM may have removed them. Check `delta.deletedFileRetentionDuration`. (3) **If VACUUM ran:** May not be able to RESTORE; ensure retention is long enough. (4) **Alternative:** Create new table from `SELECT * FROM t VERSION AS OF n` and swap.

**Mistakes:** Running VACUUM too aggressively; not knowing retention; assuming infinite history.

---

## 10. Two users need different row access on same table

**Problem:** User A sees region=US only; User B sees all.

**Good:** Use Row-Level Security (RLS). Create filter function.

**Great:** (1) **RLS** in Unity Catalog—create filter function (e.g., `region = current_user_region()`). (2) **Attach** to table: `ALTER TABLE t SET ROW FILTER func ON (region)`. (3) **Grant** to users/groups. (4) **Alternative:** Create views per role; grant view access. (5) **Audit**—ensure filter is correct; test as each user.

**Mistakes:** Implementing in app code (bypass risk); not testing as different users.

---

## 11–50 (Summary format for space)

**11. Slow dimension lookup in fact join**  
Good: Broadcast dimension. Great: Broadcast if <10MB; otherwise partition both by key; Z-ORDER fact by dimension key. Mistakes: Not checking size; shuffle when broadcast would work.

**12. Pipeline needs to run on multiple clouds**  
Good: Abstract paths; use config. Great: External locations per cloud; same catalog logic; config for storage paths; secrets per cloud. Mistakes: Hardcoding paths; cloud-specific APIs in code.

**13. Job cluster startup takes 10 minutes**  
Good: Use cluster pool. Great: Pools pre-provision; attach instead of provision; or use existing all-purpose for dev. Mistakes: Cold start acceptable; not using pools for frequent jobs.

**14. Need to pass secret to notebook**  
Good: dbutils.secrets.get. Great: Create scope; store secret; reference in notebook; never log. Cluster needs scope access. Mistakes: Hardcoding; printing secret; wrong scope.

**15. Schema changed in source; pipeline breaks**  
Good: Use mergeSchema. Great: mergeSchema on read/write; validate new columns; update downstream. Quarantine unknown columns if needed. Mistakes: Strict enforcement without evolution; no validation.

**16. Debugging which stage is slow**  
Good: Spark UI, Stages tab. Great: Jobs→Stages; sort by duration; drill to Tasks; check task distribution (skew), shuffle read, spill. Use Spark UI SQL tab for query plan. Mistakes: Guessing; not looking at task level.

**17. Reduce cost of dev clusters**  
Good: Use smaller clusters; autoscaling; terminate when idle. Great: Job clusters for scheduled; autoscaling; spot instances; cluster policies; pool for fast startup. Mistakes: Always-on large clusters; no autoscaling.

**18. Data quality failures blocking pipeline**  
Good: Quarantine bad rows. Great: Expectations with ON VIOLATION DROP ROW or quarantine table; alert on quarantine count; fix and re-ingest. Don't fail entire pipeline. Mistakes: Fail on first bad row; no quarantine; no alert.

**19. Need to orchestrate Databricks + Snowflake**  
Good: Use Airflow or ADF. Great: External orchestrator; Databricks Run Submit for Databricks tasks; Snowflake operator; single DAG; pass params. Mistakes: Trying to do in Workflows only; tight coupling.

**20. SLA: data must be fresh by 8 AM**  
Good: Schedule job; alert on failure. Great: Job by 7 AM; SLA check at 8:05; compare completion time; alert on breach; runbook. Track in metrics table. Mistakes: No SLA check job; only failure alert; no runbook.

**21. Thousands of partitions; OPTIMIZE slow**  
Good: OPTIMIZE with WHERE. Great: Incremental OPTIMIZE by partition; `WHERE date >= 'X'`; schedule; avoid full table. Consider reducing partition granularity long-term. Mistakes: Full OPTIMIZE on huge table; over-partitioning.

**22. Photon not accelerating query**  
Good: Check cluster has Photon; check compatibility. Great: Ensure Photon workers; some ops not supported—fallback to Spark; check Spark UI for engine. Upgrade Spark/Databricks. Mistakes: Assuming all queries use Photon; wrong cluster config.

**23. Grant analyst read-only to one schema**  
Good: GRANT USAGE and SELECT. Great: USAGE on catalog and schema; SELECT on schema or tables; use group. `GRANT SELECT ON ALL TABLES IN SCHEMA x TO group`. Mistakes: Forgetting USAGE; granting MODIFY.

**24. Ingestion from 100 different S3 paths**  
Good: Loop or multi-source. Great: Single path with wildcard if possible; or foreach path in workflow; single bronze table with source column; COPY INTO or Auto Loader per path. Mistakes: 100 separate jobs; no source attribution.

**25. Delta table has wrong schema; need to fix**  
Good: overwriteSchema or create new table. Great: overwriteSchema for full replace (backup first); or create new table from SELECT with cast; swap; migrate. Validate downstream. Mistakes: No backup; breaking downstream.

**26. foreachBatch MERGE very slow**  
Good: Reduce batch size; optimize MERGE. Great: Partition target; Z-ORDER; batch size (not too small = many merges); OPTIMIZE target; check skew in source batches. Mistakes: Huge batches; unoptimized target.

**27. Need to run same notebook with different params**  
Good: Widgets; job parameters. Great: dbutils.widgets; map job params to widgets; Run Submit API with notebook_params; workflow with multiple tasks. Mistakes: Copying notebooks; hardcoding.

**28. Audit: who queried PII table**  
Good: Unity Catalog audit logs. Great: Enable audit; export to Azure Monitor/S3; query logs; filter by table, user. Retention per policy. Mistakes: No audit enabled; no export; short retention.

**29. Repo conflict: edited in workspace and Git**  
Good: Resolve manually; pull/merge. Great: Decide source of truth (usually Git); sync; resolve conflicts; avoid editing same file in both. Use branches. Mistakes: Overwriting; losing changes; no process.

**30. Delete 1M rows from Delta table**  
Good: DELETE WHERE; ensure predicate uses partition. Great: Partition and Z-ORDER by filter column; DELETE with predicate; OPTIMIZE after. Batch deletes if very large. Mistakes: DELETE without predicate; no partition pruning.

**31. Stream from Kafka; need exactly-once**  
Good: Checkpoint; idempotent sink. Great: Kafka offset in checkpoint; idempotent sink (Delta with MERGE); enable Kafka idempotent producer if writing back. Exactly-once = checkpoint + idempotent. Mistakes: Append only; no idempotency.

**32. Multi-tenant: isolate tenant data**  
Good: RLS by tenant_id. Great: RLS filter `tenant_id = current_user_tenant()`; or separate schema/table per tenant; or single table with RLS. Grant per tenant. Mistakes: No RLS; app-level only; cross-tenant leak.

**33. Job fails intermittently (transient)**  
Good: Add retries. Great: Retries (3, exponential backoff); idempotent logic; identify cause (network, throttling); fix if possible. Alert on repeated failure. Mistakes: No retries; non-idempotent; ignoring root cause.

**34. Need to migrate from Hive to Unity Catalog**  
Good: Create UC tables; migrate data. Great: Plan; create catalogs/schemas; register tables (CREATE TABLE AS SELECT or SYNC); migrate permissions; validate; cutover. Use migration tools if available. Mistakes: Big bang; no validation; permission gaps.

**35. Large broadcast causing OOM**  
Good: Don't broadcast; use sort-merge. Great: Check table size; increase threshold only if truly small; otherwise sort-merge; pre-partition both; consider splitting broadcast. Mistakes: Blindly increasing threshold; broadcasting large table.

**36. COPY INTO re-copying same files**  
Good: Check path; COPY is idempotent by default. Great: COPY tracks path/size/mtime; if file changed, re-copies. Ensure source stable. Check for symlinks or moving files. Mistakes: Modifying files after copy; wrong path.

**37. Workflow task order wrong**  
Good: Set dependencies. Great: Task B "depends on" A; Workflows DAG; parallel branches by depending on same upstream; use run_if for conditional. Validate in UI. Mistakes: No dependencies; circular; wrong order.

**38. Pipeline runs in dev; fails in prod**  
Good: Check config; credentials; data. Great: Diff config (catalog, cluster, secrets, paths); prod-specific data (volume, schema); permissions; init scripts. Use same code; different config. Mistakes: Hardcoded dev values; no prod testing.

**39. Need to mask SSN for analysts**  
Good: CLS or view with mask. Great: Delta CLS mask function; or view with `CASE WHEN has_privilege THEN ssn ELSE '***' END`; grant view to analysts. RLS if row-level. Mistakes: Exposing in view; app-level only.

**40. Small files from streaming; can't OPTIMIZE during stream**  
Good: optimizeWrite; coalesce in foreachBatch. Great: delta.autoOptimize.optimizeWrite; coalesce in foreachBatch before write; schedule OPTIMIZE during low-traffic window. Mistakes: OPTIMIZE while streaming (possible but heavy); no optimizeWrite.

**41. Join key has many nulls; skew**  
Good: Filter nulls; handle separately. Great: Filter `WHERE key IS NOT NULL` before join; process nulls in separate path (e.g., left join for nulls); or coalesce null to a sentinel. Reduces skew. Mistakes: Joining with nulls; one partition for all nulls.

**42. dbt on Databricks**  
Good: dbt-databricks adapter; run via task. Great: Adapter; Delta support; incremental models; Workflows task; schema in UC; test with dbt test. Mistakes: Wrong adapter; not using Delta; no incremental.

**43. Need to run Python script in workflow**  
Good: Python task type. Great: Add Python script task; specify script path (repo or workspace); use Spark or plain Python; pass params via task params. Mistakes: Using notebook for script; wrong path.

**44. Table has 10K files; read slow**  
Good: OPTIMIZE. Great: OPTIMIZE to compact; enable optimizeWrite for future; Z-ORDER for filters; partition pruning. Consider partition count. Mistakes: Only OPTIMIZE once; not fixing write path.

**45. Column added to source; need in Silver**  
Good: mergeSchema on read and write. Great: mergeSchema; backfill new column (UPDATE or re-ingest); update downstream; validate. Document. Mistakes: overwriteSchema (loses data); no backfill.

**46. Alert on quarantine count spike**  
Good: Query quarantine table; alert if > threshold. Great: Metric: count from quarantine; workflow or scheduled job checks; alert (email, webhook) if > N; include in dashboard. Runbook for investigation. Mistakes: No alert; no threshold; no runbook.

**47. Two jobs need same cluster**  
Good: Existing cluster; both use it. Great: All-purpose cluster; or job cluster per job (recommended for isolation); or shared job cluster with task concurrency. Consider cost vs startup. Mistakes: Over-subscribing; no concurrency control.

**48. Need to sync Delta to Snowflake**  
Good: Export to S3; Snowflake external stage; copy. Great: Delta on S3; Snowflake can read Delta (via connector) or use export to Parquet; incremental via CDF or timestamp; schedule. Or Fivetran/dbt. Mistakes: Full refresh always; no incremental.

**49. Cluster policy to limit cost**  
Good: Max nodes; instance types. Great: Policy: max workers, allowed instance types, autoscaling; apply to users; prevent oversized clusters. Use cluster policies in UC. Mistakes: No policy; users create huge clusters.

**50. Validate data after migration**  
Good: Row count; checksum. Great: Row count; checksum (hash of columns); sample comparison; schema diff; null rate; duplicate check. Automate in CI. Document. Mistakes: No validation; only row count; manual only.
