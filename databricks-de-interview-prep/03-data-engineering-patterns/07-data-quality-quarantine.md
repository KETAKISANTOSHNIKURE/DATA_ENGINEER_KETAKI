# Data Quality and Quarantine

## ✅ What you need to say in interview

- **Data quality:** Validation (nulls, types, ranges, referential integrity). **Quarantine:** Bad rows go to a **separate table**; good rows to main table. Don't fail entire pipeline.
- **Techniques:** (1) **Expectations** (Great Expectations, Delta Live Tables expectations). (2) **Filter + quarantine write.** (3) **Alert** on quarantine count.
- **Resolution:** Fix source or rules; re-process quarantined rows when fixed.

## ⚙️ How it actually works

1. Apply validation (e.g., `WHERE col IS NOT NULL AND col > 0`).
2. Good rows → main table; bad rows → quarantine table (with reason, timestamp).
3. Alert if quarantine count > threshold.
4. Periodically review; fix and merge back.

## ✅ When to use

- Production pipelines where bad data shouldn't block good data.
- Audit trail of rejected rows.
- SLA on data availability (good data flows; bad data isolated).

## ❌ When to NEVER use

- Don't silently drop bad rows without quarantine—lose data, no audit.
- Don't fail entire pipeline for one bad row if you can quarantine.
- Avoid over-constraining—false positives in quarantine.

## 🚩 Common interview pitfalls

- Failing entire batch vs quarantining.
- No alerting on quarantine—bad data accumulates unseen.
- No process to fix and re-ingest quarantined data.

## 💻 Working example (SQL + PySpark)

```python
# Split good vs bad
from pyspark.sql.functions import when, col
valid = df.filter(col("amount").isNotNull() & (col("amount") > 0))
invalid = df.filter(col("amount").isNull() | (col("amount") <= 0)).withColumn("reason", lit("invalid_amount"))

valid.write.format("delta").mode("append").saveAsTable("silver_orders")
invalid.withColumn("quarantined_at", current_timestamp()).write.format("delta").mode("append").saveAsTable("quarantine_orders")
```

```sql
-- DLT expectations
CREATE LIVE TABLE silver_orders
AS SELECT * FROM bronze_orders
WHERE EXPECT (amount > 0) ON VIOLATION DROP ROW;
-- Or: ON VIOLATION FAIL UPDATE (custom)
```

## ❔ Actual interview questions + ideal answers

**Q: How do you handle bad data in a pipeline?**

- **Junior:** Validate and reject. Send bad rows to a quarantine table.
- **Senior:** **Validate** (nulls, types, business rules). **Quarantine** bad rows to a separate table with reason and timestamp—don't fail the entire pipeline. **Alert** when quarantine count exceeds threshold. **Good rows** flow to Silver/Gold. Periodically **review quarantine**, fix rules or source, **re-process** and merge back. Use **expectations** (e.g., DLT) for declarative checks.

**Q: Why quarantine instead of failing the pipeline?**

- **Junior:** So good data still gets through.
- **Senior:** **Availability:** one bad row shouldn't block millions of good rows. **Audit:** quarantine preserves rejected data for investigation. **SLA:** downstream consumers get data on time. **Recoverability:** once fixed, quarantined rows can be re-ingested. Failing the entire pipeline causes delay and requires full re-run.

---

## 5-Minute Revision Cheat Sheet

- Validate; good → main, bad → quarantine.
- Alert on quarantine.
- Don't fail entire pipeline.
- Re-process quarantine when fixed.
