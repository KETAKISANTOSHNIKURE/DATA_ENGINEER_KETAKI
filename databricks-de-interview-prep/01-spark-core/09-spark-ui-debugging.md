# Spark UI and Debugging

## ✅ What you need to say in interview

- **Spark UI:** Web UI for **Jobs**, **Stages**, **Storage**, **Executors**, **SQL**.
- **Jobs tab:** See jobs, stages, DAG. Identify **which stage is slow**.
- **Stages tab:** **Task duration**, **shuffle read/write**, **GC time**, **spill**.
- **Executors tab:** Memory, disk, failures.

## ⚙️ How it actually works

- Driver hosts Spark UI (port 4040 by default).
- Metrics updated as tasks complete.
- Event log persisted for finished applications (e.g., `spark.eventLog.enabled`).

## ✅ When to use

- Debugging slow jobs: find slow stage → slow tasks → root cause (skew, shuffle, spill).
- Tuning: check partition count, shuffle size, GC.

## ❌ When to NEVER use

- Don't ignore task duration distribution—uniform = good; skewed = problem.
- Don't skip executor tab when debugging OOM.

## 🚩 Common interview pitfalls

- Not knowing where to look: Jobs → Stages → Tasks.
- Missing spill (disk) as a sign of memory pressure.
- Confusing shuffle read size with input size.

## 💻 Working example (PySpark)

**In Databricks:** Cluster → Spark UI, or click "View Spark UI" on a running job.

**Key metrics:**
- **Task duration** — if one task >> others → skew.
- **Shuffle Read** — large = expensive shuffle.
- **Spill (Memory)** — data spilled to disk = memory pressure.
- **GC Time** — high = memory churn.

## ❔ Actual interview questions + ideal answers

**Q: How do you debug a slow Spark job?**

- **Junior:** Look at Spark UI, find the slow stage.
- **Senior:** (1) **Spark UI → Jobs** — identify which stage takes longest. (2) **Stages → Tasks** — check **task duration distribution**; if one task is 10x others, it's **skew**. (3) **Shuffle read/write** — large values mean expensive shuffle. (4) **Spill** — indicates memory pressure. (5) **Executors** — OOM kills, GC time. Fix: skew → salting; shuffle → broadcast or repartition; spill → more memory or fewer partitions.

**Q: What does "Spill (Memory)" mean?**

- **Junior:** Data was written to disk because memory was full.
- **Senior:** When executor **memory is exhausted** during a task, Spark **spills** intermediate data to disk. It's a sign of **memory pressure**—either increase executor memory, reduce partition size, or optimize (e.g., avoid large shuffles, broadcast small tables). Spill slows the job due to disk I/O.

---

## 5-Minute Revision Cheat Sheet

- Jobs → Stages → Tasks.
- Slow task >> others = skew.
- Large shuffle read = expensive shuffle.
- Spill = memory pressure.
- Executors tab = OOM, GC.
