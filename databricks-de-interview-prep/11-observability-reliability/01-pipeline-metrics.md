# Pipeline Metrics

## ✅ What you need to say in interview

- **Pipeline metrics:** Track **row counts**, **duration**, **success/failure**, **data freshness**, **data quality** (null rate, duplicates).
- **Where:** **Delta Live Tables** events, **custom metrics table** (job writes counts, timestamps), **Spark listener** (task metrics), **Datadog/Prometheus** (export).
- **Use:** Dashboards, alerting, SLA tracking, debugging.
- **Key metrics:** Rows read/written, processing time, failure rate, latency (data arrival → table update).

## ⚙️ How it actually works

1. Job runs; at end, write metrics to table (e.g., `pipeline_runs`: job_id, run_id, rows_in, rows_out, duration, status, timestamp).
2. Or: use Spark listener to capture task/job metrics.
3. DLT: built-in event log (row counts, expectations).
4. External: push to Datadog/Prometheus via API or agent.

## ✅ When to use

- All production pipelines.
- Track trends (row growth, duration).
- Alert on anomalies (sudden drop in rows, long duration).
- Data observability (freshness, quality).

## ❌ When to NEVER use

- Don't track metrics without alerting—waste.
- Don't store PII in metrics.
- Avoid high-cardinality dimensions (explosion).
- Don't block pipeline on metrics write—async if possible.

## 🚩 Common interview pitfalls

- No metrics = flying blind.
- Only tracking success/fail—need row counts, duration.
- Metrics in different system than alerts—integration complexity.

## 💻 Working example (SQL + PySpark)

```python
# Custom metrics
metrics = {
    "job": "silver_orders",
    "run_id": run_id,
    "rows_read": bronze_count,
    "rows_written": silver_count,
    "duration_sec": duration,
    "status": "success",
    "timestamp": current_timestamp()
}
spark.createDataFrame([metrics]).write.format("delta").mode("append").saveAsTable("pipeline_metrics")
```

## ❔ Actual interview questions + ideal answers

**Q: What metrics do you track for a data pipeline?**

- **Junior:** Row counts, duration, success/fail.
- **Senior:** **Volume:** rows read, rows written—detect drops or spikes. **Duration:** job run time—catch slowdowns. **Status:** success/failure—alert on fail. **Freshness:** max(timestamp) in table—SLA. **Quality:** null rate, duplicate count (from expectations). Store in **metrics table** or push to **Datadog/Prometheus**. Use for **dashboards** and **alerting** (e.g., rows < threshold, duration > SLA).

**Q: How do you implement pipeline metrics in Databricks?**

- **Junior:** Write metrics to a Delta table at end of job.
- **Senior:** At **end of job**, write to a **metrics table** (job, run_id, rows_in, rows_out, duration, status, timestamp). **DLT** has built-in event log. For **Spark metrics**, use **SparkListener** or **Spark UI** (for ad-hoc). **Export** to Datadog/Prometheus for centralized monitoring. **Alert** on thresholds (e.g., failure, row count drop > 10%). Use **workflow notification** for job failure; custom alert for metrics.

---

## 5-Minute Revision Cheat Sheet

- Rows, duration, status, freshness.
- Metrics table or external.
- Alert on anomalies.
- DLT has built-in events.
