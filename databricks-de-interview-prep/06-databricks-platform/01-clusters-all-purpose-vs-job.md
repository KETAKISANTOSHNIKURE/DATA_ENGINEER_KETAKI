# Clusters: All-Purpose vs Job

## ✅ What you need to say in interview

- **All-Purpose (Interactive):** For **ad-hoc** work. Users **attach** and run notebooks. Cluster stays up; **shared** by team. Billed while running.
- **Job cluster:** **Ephemeral**. Created for a **specific job**; **terminates** when job completes. No interactive attach. **Cost-effective** for scheduled/automated jobs.
- **When:** Use **Job** for workflows, ETL, scheduled pipelines. Use **All-Purpose** for development, exploration, dashboards.

## ⚙️ How it actually works

- All-Purpose: you start; you stop. Multiple users can attach.
- Job: Workflows create cluster, run tasks, terminate. Cluster config in job definition.
- Job clusters can use **cluster pools** for faster startup.

## ✅ When to use

- **Job:** Production ETL, scheduled jobs, CI/CD runs.
- **All-Purpose:** Dev, ad-hoc queries, collaborative work.

## ❌ When to NEVER use

- Don't use All-Purpose for scheduled production jobs—costly, manual.
- Don't use Job for interactive development—cluster dies after run.
- Don't leave All-Purpose clusters running overnight if not needed.

## 🚩 Common interview pitfalls

- Confusing which cluster type for which use case.
- Not knowing Job clusters are ephemeral.
- Job clusters can't be attached for debugging (use All-Purpose for dev).

## 💻 Working example (SQL + PySpark)

```python
# Job cluster: configured in Workflows UI or API
# All-Purpose: start from Clusters UI, attach notebook
# No code difference—same Spark API
```

## ❔ Actual interview questions + ideal answers

**Q: What is the difference between All-Purpose and Job clusters?**

- **Junior:** All-Purpose for interactive; Job for automated jobs.
- **Senior:** **All-Purpose** clusters are for **interactive** use—users attach notebooks, run ad-hoc queries. Cluster runs until stopped; **shared**. **Job** clusters are **ephemeral**—created for a workflow task, run the job, **terminate** when done. No interactive attach. Use Job for **production ETL/scheduled jobs**—pay only for job duration. Use All-Purpose for **development and exploration**.

**Q: When would you use a Job cluster over All-Purpose?**

- **Junior:** For scheduled or automated pipelines.
- **Senior:** For **scheduled workflows**, **CI/CD** runs, **batch ETL**—Job clusters are **cost-effective** because they run only during the job. No idle time. All-Purpose would require keeping a cluster up 24/7 or manual start/stop. Job clusters also support **cluster pools** for faster startup by pre-warming nodes.

---

## 5-Minute Revision Cheat Sheet

- All-Purpose: interactive, shared, manual.
- Job: ephemeral, one job, auto-terminate.
- Job for production ETL; All-Purpose for dev.
