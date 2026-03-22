# Final Interview Checklist — 24 Hours Before

**No explanations. Tick as you go.**

---

## Spark Core
- [ ] Driver vs Executor roles
- [ ] Job → Stage → Task hierarchy
- [ ] Narrow vs Wide transformations
- [ ] Lazy evaluation
- [ ] repartition vs coalesce
- [ ] Broadcast vs Sort-Merge join
- [ ] Cache vs Persist levels
- [ ] AQE (coalesce, skew, DPP)

## Delta Lake
- [ ] Transaction log / ACID
- [ ] Schema enforcement vs evolution
- [ ] Time travel / RESTORE
- [ ] MERGE INTO syntax
- [ ] OPTIMIZE + Z-ORDER
- [ ] VACUUM retention
- [ ] Delete/Update performance

## Data Engineering Patterns
- [ ] Bronze → Silver → Gold
- [ ] Idempotent write pattern
- [ ] Incremental load (timestamp vs CDC)
- [ ] Deduplication (MERGE, window)
- [ ] Late-arriving data handling
- [ ] Backfill strategy
- [ ] Data quality / quarantine

## Structured Streaming
- [ ] Microbatch model
- [ ] Checkpoint location
- [ ] Append vs Complete vs Update mode
- [ ] Watermark + late data
- [ ] foreachBatch for batch sinks
- [ ] Streaming CDC to Delta

## Performance
- [ ] Reduce shuffle
- [ ] Partition sizing (128MB–200MB)
- [ ] Small files problem
- [ ] Data skew (salting, AQE)
- [ ] Partitioning strategy
- [ ] Photon runtime

## Databricks Platform
- [ ] All-Purpose vs Job clusters
- [ ] Autoscaling
- [ ] dbutils (fs, notebook, widgets, secrets)
- [ ] Secrets (scope, key)
- [ ] Init scripts, cluster libraries

## Unity Catalog
- [ ] Catalog → Schema → Table
- [ ] Grants (SELECT, MODIFY, etc.)
- [ ] RLS / CLS
- [ ] Lineage, audit

## Orchestration
- [ ] Workflows (tasks, dependencies)
- [ ] Parameters, retries, alerting
- [ ] External: Airflow, ADF

## Ingestion
- [ ] Auto Loader (cloudFiles, schema evolution)
- [ ] COPY INTO
- [ ] Landing zone design

## DevOps
- [ ] Repos, Git integration
- [ ] CI/CD patterns
- [ ] Dev → Staging → Prod

## Observability
- [ ] Pipeline metrics
- [ ] SLA monitoring

## Question Bank
- [ ] Reviewed 150 rapid-fire
- [ ] Reviewed 50 scenario Qs
- [ ] Ran through mock interview

## Logistics
- [ ] Stable internet
- [ ] Camera/mic test
- [ ] Quiet space
- [ ] Water, notes, pen
