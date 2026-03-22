# dbutils

## ✅ What you need to say in interview

- **dbutils:** Databricks **utilities** for filesystem, notebooks, widgets, secrets, and more.
- **dbutils.fs:** File operations—`ls`, `cp`, `mv`, `rm`, `mount`, `head`, `put`. Works with DBFS and cloud paths.
- **dbutils.notebook:** Run another notebook—`run(path, timeout, arguments)`. Returns (exitValue, results).
- **dbutils.widgets:** Parameterize notebooks—`text`, `dropdown`, `multiselect`, `get`.
- **dbutils.secrets:** Access secrets—`get(scope, key)`. Never log secrets.

## ⚙️ How it actually works

- dbutils is available in all Databricks notebooks and jobs.
- fs: wraps DBFS and cloud storage APIs.
- notebook.run: executes notebook as subprocess; can pass params.
- secrets: fetches from Azure Key Vault, AWS Secrets Manager, or Databricks-backed scope.

## ✅ When to use

- **fs:** Inspect paths, copy files, manage mounts.
- **notebook.run:** Orchestrate multi-notebook jobs; reuse logic.
- **widgets:** Parameterize for workflows (e.g., date param).
- **secrets:** Credentials, API keys.

## ❌ When to NEVER use

- Don't log or print `dbutils.secrets.get`—exposes secrets.
- Don't use dbutils in non-Databricks Spark—not available.
- Avoid hardcoding paths; use widgets or config.

## 🚩 Common interview pitfalls

- Confusing dbutils.fs with os (use dbutils.fs for DBFS).
- Not knowing widgets for parameterization.
- Printing secrets.

## 💻 Working example (SQL + PySpark)

```python
# Filesystem
dbutils.fs.ls("/mnt/data/")
dbutils.fs.cp("s3://bucket/a", "dbfs:/mnt/a")
dbutils.fs.head("/path/file.json", maxBytes=1000)

# Notebook
result = dbutils.notebook.run("/path/notebook", 3600, {"date": "2024-01-01"})

# Widgets
dbutils.widgets.text("date", "2024-01-01")
dbutils.widgets.dropdown("env", "dev", ["dev", "prod"])
date = dbutils.widgets.get("date")

# Secrets
api_key = dbutils.secrets.get(scope="my-scope", key="api-key")
```

## ❔ Actual interview questions + ideal answers

**Q: What is dbutils and what do you use it for?**

- **Junior:** Databricks utilities for files, notebooks, secrets.
- **Senior:** **dbutils** provides Databricks-specific utilities: **fs** for file ops (ls, cp, mv, mount) on DBFS/cloud; **notebook.run** to invoke other notebooks with params; **widgets** to parameterize notebooks (text, dropdown); **secrets** to access credentials. Use fs for paths, notebook.run for orchestration, widgets for workflow params, secrets for API keys. **Never log secrets.**

**Q: How do you pass parameters to a Databricks job?**

- **Junior:** Use widgets or job parameters.
- **Senior:** **Workflow parameters** are passed as `widgets`—define in notebook with `dbutils.widgets.text("param", default)`, then set in job definition. Or use **notebook.run** with a dict of arguments. For **Python** jobs, use `dbutils.widgets.get("param")` to read. Parameters can also be passed via **task parameters** in Workflows and accessed the same way.

---

## 5-Minute Revision Cheat Sheet

- dbutils.fs: ls, cp, mv, head.
- dbutils.notebook.run: run notebook with args.
- dbutils.widgets: parameterize.
- dbutils.secrets.get: credentials; never log.
