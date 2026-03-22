# Init Scripts and Libraries

## ✅ What you need to say in interview

- **Init scripts:** **Bash scripts** that run on each node at **cluster startup** (before Spark). Use to install packages, set env vars, mount storage.
- **Scope:** Cluster-level or global (all clusters). Stored in DBFS or workspace files.
- **Libraries:** **Python/Jar/R** packages. Attach at **cluster level** (all notebooks) or **notebook level** (session). Sources: PyPI, Maven, CRAN, or upload.
- **Cluster libraries vs notebook:** Cluster = persistent for cluster lifetime; notebook = session-scoped (e.g., %pip).

## ⚙️ How it actually works

1. Init script: cluster starts → run script on driver and workers → then Spark starts.
2. Cluster libraries: installed when cluster starts; available to all attached sessions.
3. %pip in notebook: installs in current session only.
4. Job with library: job cluster gets libraries from cluster config.

## ✅ When to use

- **Init script:** System-level setup (apt, env vars), custom Java, mount scripts.
- **Cluster libraries:** Production dependencies; same for all workloads on cluster.
- **%pip:** Ad-hoc package try; dev only.

## ❌ When to NEVER use

- Don't use init script for Python packages—use libraries.
- Don't put long-running or fragile logic in init scripts—slows startup, hard to debug.
- Don't mix cluster libs and %pip for same package—version conflicts.
- Avoid init script for secrets (use cluster env + secrets).

## 🚩 Common interview pitfalls

- Init script vs library—init for system; library for Python/JVM.
- Notebook %pip doesn't persist across sessions on same cluster (unless notebook lib).
- Init script failure = cluster fails to start.

## 💻 Working example (SQL + PySpark)

```bash
#!/bin/bash
# Init script (e.g., dbfs:/databricks/scripts/init.sh)
apt-get update && apt-get install -y some-tool
echo "export MY_VAR=value" >> /etc/profile
```

```python
# Cluster config: Init script path
# dbfs:/databricks/scripts/init.sh

# Cluster libraries: PyPI
# pandas==2.0.0

# Notebook
%pip install ad-hoc-package  # session only
```

## ❔ Actual interview questions + ideal answers

**Q: What is an init script and when do you use it?**

- **Junior:** A script that runs when the cluster starts. Use for installing system packages.
- **Senior:** **Init scripts** are **bash scripts** that run on each node at **cluster startup**, before Spark. Use for **system-level** setup: install apt packages, set environment variables, configure JVM, run mount scripts. For **Python packages**, use **cluster libraries** instead. Init scripts are cluster-scoped or global. Store in DBFS; failure in init script fails cluster start.

**Q: Cluster libraries vs %pip install—when to use which?**

- **Junior:** Cluster libraries for production; %pip for trying things.
- **Senior:** **Cluster libraries** are installed at cluster start and available to **all** sessions—use for **production dependencies**. **%pip** installs in the **current session**—use for ad-hoc experimentation. For **jobs**, specify libraries in job cluster config so they're installed consistently. Don't mix—can cause version conflicts. Prefer cluster libraries for reproducibility.

---

## 5-Minute Revision Cheat Sheet

- Init script: bash at startup; system-level.
- Cluster libs: PyPI, Maven; all sessions.
- %pip: session-scoped; ad-hoc.
- Init for system; libs for packages.
