# 06 — Databricks Platform

**Interview weight:** High. Platform-specific knowledge.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | Clusters: All-Purpose vs Job | Critical |
| 02 | Autoscaling, node types, pools | Critical |
| 03 | dbutils | Critical |
| 04 | Secrets management | Critical |
| 05 | Init scripts, libraries | High |

## 5-Minute Revision Cheat Sheet

- **All-Purpose:** Interactive; shared; users attach. **Job:** Ephemeral; one job; terminate after.
- **Autoscaling:** Min/max workers; scale based on load.
- **dbutils:** fs, notebook, widgets, secrets.
- **Secrets:** Scopes (secret scope); keys; reference via `dbutils.secrets.get`.
- **Init scripts:** Run at cluster start; install libs, config.
- **Libraries:** Cluster-level or notebook-level (PyPI, Maven, etc.).
