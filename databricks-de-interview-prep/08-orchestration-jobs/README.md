# 08 — Orchestration and Jobs

**Interview weight:** Medium–High.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | Databricks Workflows | Critical |
| 02 | Parameters, retries, alerting | Critical |
| 03 | External orchestration (Airflow, ADF) | High |

## 5-Minute Revision Cheat Sheet

- **Workflows:** Jobs = tasks + dependencies. Notebook, Python, JAR, SQL. DAG.
- **Parameters:** Widgets; job/task params; pass between tasks.
- **Retries:** Per task; exponential backoff.
- **Alerting:** On failure/success; email, Slack, webhook.
- **External:** Airflow, ADF call Databricks via API/Run Submit.
