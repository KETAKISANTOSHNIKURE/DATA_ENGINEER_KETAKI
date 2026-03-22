# Parameters, Retries, Alerting

## ✅ What you need to say in interview

- **Parameters:** **Job-level** or **task-level**. Pass to notebooks via widgets (`dbutils.widgets.get`). Used for date, env, config. Can use **run job** API to pass params.
- **Retries:** Per-task. **Max retries**, **retry interval** (min). **Exponential backoff** optional. Retry on failure (transient) or always.
- **Alerting:** **On failure**, **on success**, **on timeout**. **Email**, **Slack**, **webhook**, **PagerDuty**. Configure in job settings.
- **Timeout:** Per-task or per-job. Cancel if exceeded.

## ⚙️ How it actually works

1. Params: job run can override; passed to notebook as widget values.
2. Retry: task fails → wait → retry. After max, job fails.
3. Alert: trigger sends notification. Webhook can integrate with incident tools.
4. Timeout: task/job cancelled; marked failed.

## ✅ When to use

- **Params:** Date range, environment (dev/prod), table names.
- **Retries:** Transient failures (network, throttling). 2–3 retries typical.
- **Alerting:** Production jobs—notify on failure.
- **Timeout:** Prevent hung jobs.

## ❌ When to NEVER use

- Don't retry indefinitely—mask bugs.
- Don't skip alerting for production.
- Don't hardcode params—use job parameters.
- Avoid very short retry intervals (thundering herd).

## 🚩 Common interview pitfalls

- Params not reaching notebook (check widget names).
- Retry on same bad data—idempotency critical.
- Alert fatigue—tune thresholds.

## 💻 Working example (SQL + PySpark)

```python
# In notebook
date = dbutils.widgets.get("date")  # from job param
env = dbutils.widgets.get("env", "prod")
```

```json
// Job config
{
  "tasks": [{
    "task_key": "ingest",
    "notebook_task": {...},
    "max_retries": 3,
    "retry_on_timeout": true,
    "timeout_seconds": 3600
  }],
  "email_notifications": {"on_failure": ["team@company.com"]},
  "webhook_notifications": {"on_failure": {"id": "slack-webhook"}}
}
```

## ❔ Actual interview questions + ideal answers

**Q: How do you pass parameters to a Databricks job?**

- **Junior:** Use job parameters; read in notebook with dbutils.widgets.get.
- **Senior:** Define **job parameters** (or task overrides) in the job config. Map to **notebook widgets**—e.g., param `date` → widget `date`. In notebook: `dbutils.widgets.get("date")`. Can also use **Run Submit** API to pass params per run. Use for **date**, **environment**, **config**—makes job reusable and testable.

**Q: How do you handle transient failures in a job?**

- **Junior:** Use retries with backoff.
- **Senior:** Configure **per-task retries**—e.g., max 3, with **min interval** (or exponential backoff). For **transient** failures (network, throttling), retries often succeed. Ensure **idempotency**—retry should produce same result. For **persistent** failures (bad data), retries won't help—alert and fix. Use **timeout** to prevent hung tasks from retrying forever.

---

## 5-Minute Revision Cheat Sheet

- Params → widgets.
- Retries: max 3, backoff.
- Alert on failure.
- Timeout to prevent hangs.
