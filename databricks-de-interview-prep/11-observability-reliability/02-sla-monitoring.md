# SLA Monitoring

## ✅ What you need to say in interview

- **SLA:** **Service Level Agreement**—e.g., "Silver table refreshed by 8 AM daily." Monitor and **alert** when breached.
- **Monitoring:** Track **actual completion time** vs **SLA target**. Compare `max(data_timestamp)` or `job_end_time` with SLA (e.g., 8 AM).
- **Alerting:** On SLA breach—email, PagerDuty, Slack. Escalate if repeated.
- **Pattern:** Job writes completion time; monitoring job or dashboard compares to SLA; triggers alert.

## ⚙️ How it actually works

1. Define SLA: e.g., "daily job completes by 8 AM" or "data fresh within 1 hour."
2. Job writes completion metadata (end time, max data timestamp).
3. Monitoring: cron job or dashboard checks "did job X complete by 8 AM?" If not, trigger alert.
4. Use Workflows alert on failure; for SLA (time-based), need custom check.

## ✅ When to use

- Production pipelines with commitments.
- Data freshness guarantees.
- Escalation paths.

## ❌ When to NEVER use

- Don't set SLA without monitoring.
- Don't ignore repeated breaches—root cause.
- Avoid vague SLAs ("as soon as possible").
- Don't alert without runbook.

## 🚩 Common interview pitfalls

- SLA vs job failure—SLA = time; failure = success/fail.
- No runbook for alerts.
- Monitoring job itself can fail—redundancy.

## 💻 Working example (SQL + PySpark)

```python
# SLA check job (runs at 8:05 AM)
sla_time = "08:00"
job_end = spark.sql("SELECT max(end_time) FROM pipeline_runs WHERE job = 'silver' AND date = current_date()").collect()[0][0]
if job_end is None or job_end > sla_time:
    # Breach - trigger alert
    send_alert("SLA breach: silver job did not complete by 8 AM")
```

## ❔ Actual interview questions + ideal answers

**Q: How do you monitor SLA for a daily pipeline?**

- **Junior:** Check if job completed by the SLA time. Alert if not.
- **Senior:** Define **SLA** (e.g., complete by 8 AM). **Pipeline** writes `end_time` to metrics table. **Monitoring job** runs at 8:05 AM—queries metrics, checks if job completed by 8 AM. If **breach**, trigger **alert** (email, PagerDuty). Use **workflow** with schedule; task = "SLA check" notebook. For **data freshness** SLA (e.g., max event time within 1 hr of now), check `max(timestamp)` in table. Have **runbook** for alerts.

**Q: What is the difference between job failure alert and SLA alert?**

- **Junior:** Failure = job didn't succeed. SLA = didn't finish on time.
- **Senior:** **Failure alert:** Job **exits with error**—Workflows can notify on task failure. **SLA alert:** Job may **succeed** but **after** SLA time—e.g., completed at 9 AM when SLA was 8 AM. Requires **custom check**—monitoring job that compares completion time to SLA. Both important: failure = immediate; SLA = commitment to stakeholders.

---

## 5-Minute Revision Cheat Sheet

- SLA = completion time target.
- Monitor: compare actual vs target.
- Alert on breach.
- Runbook for response.
- Failure ≠ SLA (both matter).
