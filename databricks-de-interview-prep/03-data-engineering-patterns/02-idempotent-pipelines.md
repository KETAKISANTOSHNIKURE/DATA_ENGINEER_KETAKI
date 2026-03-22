# Idempotent Pipelines

## ✅ What you need to say in interview

- **Idempotent:** Running the pipeline **multiple times** with the same input produces the **same output**. No duplicates, no partial state.
- **Techniques:** (1) **MERGE** with unique key. (2) **Overwrite by partition** (e.g., `INSERT OVERWRITE ... PARTITION (date='x')`). (3) **Transactional writes** (Delta ACID).
- **Why:** Retries, backfills, re-runs must be safe.

## ⚙️ How it actually works

1. MERGE: source + target, match on key → update/insert. Same source = same result.
2. Partition overwrite: replace entire partition; re-run replaces with same data.
3. Delta: commit is atomic; failed job = no partial write.

## ✅ When to use

- All production pipelines.
- Jobs with retries.
- Backfill scenarios.

## ❌ When to NEVER use

- Don't use append-only for upserts without deduplication—creates duplicates on retry.
- Don't overwrite whole table for incremental—use partition overwrite or MERGE.
- Avoid non-deterministic logic (e.g., `current_timestamp` in key) if it breaks idempotency.

## 🚩 Common interview pitfalls

- Saying "we retry so we don't need idempotency" (retries make idempotency essential).
- Append + dedupe in same run: second run can create duplicates if dedupe window doesn't cover re-ingested data.

## 💻 Working example (SQL + PySpark)

```sql
-- Idempotent: MERGE
MERGE INTO silver_orders t USING bronze_orders_staging s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Idempotent: partition overwrite
INSERT OVERWRITE gold_daily PARTITION (date='2024-01-15')
SELECT ... FROM silver WHERE date = '2024-01-15';
```

## ❔ Actual interview questions + ideal answers

**Q: How do you make a pipeline idempotent?**

- **Junior:** Use MERGE or overwrite by partition.
- **Senior:** (1) **MERGE** for upserts—unique key ensures same source = same result. (2) **Partition overwrite** for batch—replace partition with same data on re-run. (3) **Delta ACID**—commit is atomic; failed job leaves no partial state. (4) **Deterministic** keys—no `uuid()` or `current_timestamp` in business key. Design so that re-running with same input is a no-op for correctness.

**Q: Why is idempotency important?**

- **Junior:** So retries don't create duplicates.
- **Senior:** **Retries** (network, transient failures) and **backfills** will re-process the same data. Without idempotency, you get **duplicates or inconsistent state**. Idempotency ensures **exactly-once semantics** from the pipeline's perspective—critical for financial and audit use cases.

---

## 5-Minute Revision Cheat Sheet

- Same input → same output.
- MERGE, partition overwrite.
- Delta ACID = atomic.
- No random/uuid in keys.
