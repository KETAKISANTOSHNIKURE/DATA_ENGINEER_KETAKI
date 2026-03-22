# Databricks Workflows

## ✅ What you need to say in interview

- **Workflows:** Databricks **job orchestration**. **Job** = DAG of **tasks** (notebook, Python, JAR, SQL, dbt, etc.). Tasks have **dependencies**.
- **Task types:** Notebook, Python script, JAR, Spark Submit, SQL, dbt, Wheel. Can run on **Job cluster** (ephemeral) or **existing cluster**.
- **DAG:** Define task order; parallel branches; conditional (e.g., run if previous succeeded).
- **Trigger:** Manual, schedule (cron), or event (e.g., file arrival).

## ⚙️ How it actually works

1. Job defined with tasks and dependencies.
2. On trigger, Workflows schedules tasks per DAG.
3. Each task runs on its cluster (job or shared).
4. Outputs (e.g., notebook return) can be passed to downstream tasks.
5. Failure triggers retries (if configured) and/or alerting.

## ✅ When to use

- ETL pipelines (Bronze → Silver → Gold).
- Scheduled jobs.
- Multi-step workflows with dependencies.
- Replace external orchestrator for Databricks-native flows.

## ❌ When to NEVER use

- Don't use for real-time streaming—use streaming jobs.
- Don't put long-running exploration in workflows—use interactive.
- Avoid complex branching when a simple DAG suffices.

## 🚩 Common interview pitfalls

- Confusing job with cluster—job runs tasks; cluster runs Spark.
- Not knowing task dependencies (run after).
- Each task can have its own cluster config.

## 💻 Working example (SQL + PySpark)

```python
# Workflows API / UI
# Task 1: bronze_ingest (notebook)
# Task 2: silver_transform (notebook) — depends on Task 1
# Task 3: gold_aggregate (notebook) — depends on Task 2
# Schedule: 0 6 * * * (daily 6 AM)
```

## ❔ Actual interview questions + ideal answers

**Q: What is Databricks Workflows?**

- **Junior:** Job orchestration for running notebooks and tasks in order.
- **Senior:** **Workflows** is Databricks' **native orchestrator**. A **job** is a DAG of **tasks** (notebook, Python, JAR, SQL, dbt). Tasks have **dependencies**—run after. Supports **scheduling** (cron), **parameters**, **retries**, **alerting**. Each task can use a **job cluster** (ephemeral) or **existing cluster**. Replaces need for Airflow/ADF for many Databricks-native pipelines.

**Q: How do you chain tasks in a Workflow?**

- **Junior:** Set dependencies—task B runs after task A.
- **Senior:** Define **task dependencies**—task B "depends on" task A. Workflows runs A first; when A succeeds, runs B. For **parallel** tasks, both depend on same upstream. Can pass **outputs** (e.g., notebook return value) to downstream via task values. Use **run_if** for conditional execution (e.g., only on failure of another task).

---

## 5-Minute Revision Cheat Sheet

- Job = DAG of tasks.
- Task types: notebook, Python, SQL, JAR.
- Dependencies: run after.
- Schedule, parameters, retries, alerts.
