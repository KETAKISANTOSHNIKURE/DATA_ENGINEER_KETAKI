# External Orchestration: Airflow, ADF

## ✅ What you need to say in interview

- **External orchestration:** Use **Airflow**, **Azure Data Factory**, **Prefect**, etc. to orchestrate **across** systems. Databricks is one node.
- **Pattern:** Orchestrator triggers Databricks job via **REST API** (Jobs Run Submit). Poll for completion or use webhook.
- **When:** Multi-system pipelines (Databricks + Snowflake + API); centralized orchestration; existing Airflow/ADF investment.
- **Databricks operators:** Airflow has `DatabricksSubmitRunOperator`; ADF has Databricks activity. Both call Run Submit API.

## ⚙️ How it actually works

1. Orchestrator creates a Databricks job run (API: `POST /api/2.1/jobs/run-now`).
2. Returns run_id. Orchestrator polls `GET /api/2.1/jobs/runs/get` or waits for webhook.
3. On success/failure, orchestrator proceeds to next task.
4. Pass params via API.

## ✅ When to use

- Cross-system DAGs (Databricks + DB + API).
- Centralized orchestration (one place for all pipelines).
- Compliance (orchestration must be in specific tool).
- Reuse existing Airflow/ADF.

## ❌ When to NEVER use

- Don't use external orchestration for Databricks-only pipelines when Workflows suffices—adds complexity.
- Don't poll too frequently—API rate limits.
- Avoid tight coupling—use async where possible.

## 🚩 Common interview pitfalls

- Not knowing Run Submit API is the integration point.
- Polling vs webhook (webhook more efficient).
- Credentials—use OAuth or token; store in secrets.

## 💻 Working example (SQL + PySpark)

```python
# Airflow
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
DatabricksSubmitRunOperator(
    task_id='run_notebook',
    json={
        'run_name': 'ingest',
        'notebook_task': {'notebook_path': '/path/notebook'},
        'python_params': ['2024-01-01'],
        'existing_cluster_id': 'xxx'
    },
    polling_period_seconds=30
)
```

## ❔ Actual interview questions + ideal answers

**Q: When would you use Airflow/ADF instead of Databricks Workflows?**

- **Junior:** When we have other systems in the pipeline or already use Airflow.
- **Senior:** Use **external orchestration** when: (1) **Multi-system** pipeline—Databricks + Snowflake + APIs; one DAG. (2) **Centralized** orchestration—one tool for all pipelines. (3) **Existing investment** in Airflow/ADF. (4) **Compliance**—orchestration must live in specific system. For **Databricks-only** pipelines, Workflows is simpler—no cross-system calls, native integration.

**Q: How does Airflow trigger a Databricks job?**

- **Junior:** Via the Databricks operator; it calls the API.
- **Senior:** **DatabricksSubmitRunOperator** (or equivalent) calls **Jobs Run Submit API** (`POST /api/2.1/jobs/run-now`) with job/task config and params. Returns **run_id**. Operator **polls** Runs Get API until completion, or uses **webhook** for async. Credentials via connection (token or OAuth). Pass **python_params** or **notebook_params** for notebook parameters.

---

## 5-Minute Revision Cheat Sheet

- External: Airflow, ADF.
- Integration: Run Submit API.
- Poll or webhook for completion.
- Use when multi-system or centralized.
