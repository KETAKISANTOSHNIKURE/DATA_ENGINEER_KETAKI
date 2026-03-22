# Backfill Strategy

## ✅ What you need to say in interview

- **Backfill:** Re-process **historical** data (new pipeline, fix bug, new logic).
- **Strategy:** (1) **Partition-based**—process one partition at a time. (2) **Idempotent**—overwrite partition or MERGE so re-run is safe. (3) **Parallelism**—multiple partitions in parallel if independent. (4) **Checkpointing**—track which partitions done.
- **Order:** Often newest-first (more relevant) or oldest-first (simpler dependencies).

## ⚙️ How it actually works

1. Identify partitions to backfill (e.g., date range).
2. For each partition: read source, transform, write (overwrite partition or MERGE).
3. Idempotent: same partition run twice = same result.
4. Parallel: run multiple partition jobs (e.g., in workflow).

## ✅ When to use

- New pipeline with historical data.
- Bug fix requiring re-compute.
- Schema or logic change.

## ❌ When to NEVER use

- Don't backfill without idempotent design—duplicates on retry.
- Don't backfill full table at once if huge—partition by partition.
- Avoid backfilling without testing on a subset first.

## 🚩 Common interview pitfalls

- Full table overwrite for large tables—expensive, risky.
- Not considering downstream consumers during backfill.
- No way to resume if backfill fails midway.

## 💻 Working example (SQL + PySpark)

```python
# Backfill by partition
for date in date_range:
    df = spark.read.parquet(f"/bronze/date={date}/")
    transformed = transform(df)
    transformed.write.format("delta").mode("overwrite"). \
        partitionBy("date").option("replaceWhere", f"date = '{date}'").save("/silver/")
```

```sql
-- Replace single partition
INSERT OVERWRITE silver PARTITION (date='2024-01-01')
SELECT * FROM bronze WHERE date = '2024-01-01';
```

## ❔ Actual interview questions + ideal answers

**Q: How do you backfill a Delta table?**

- **Junior:** Re-run the pipeline for the date range. Use overwrite by partition.
- **Senior:** **Partition-based backfill:** iterate over partitions (e.g., dates), read source, transform, **overwrite that partition** or **MERGE** into target. **Idempotent** so retries are safe. Run partitions in **parallel** (workflow tasks) if independent. **replaceWhere** in Delta ensures only that partition is overwritten. Test on one partition first. Track progress (e.g., table of completed partitions) for resume.

**Q: What if the backfill fails halfway?**

- **Junior:** Retry. It should be idempotent.
- **Senior:** With **idempotent** design (partition overwrite or MERGE), retrying is safe. Maintain a **checkpoint** (e.g., table of completed partition values) so you can **resume** from where it failed instead of redoing everything. Use workflow **retries** for transient failures; for logic bugs, fix and resume from checkpoint.

---

## 5-Minute Revision Cheat Sheet

- Partition-based, idempotent.
- Overwrite partition or MERGE.
- Parallelize by partition.
- Checkpoint for resume.
