# 01 — Spark Core

**Interview weight:** Highest. Every Databricks interview starts here.

## Files (order matters)

| # | Topic | Must-know level |
|---|-------|-----------------|
| 01 | Driver-Executor model | Critical |
| 02 | Job-Stage-Task | Critical |
| 03 | Transformations, Actions, Lazy eval | Critical |
| 04 | Narrow vs Wide, Shuffle | Critical |
| 05 | Partitions, coalesce, repartition | Critical |
| 06 | Joins (broadcast, sort-merge) | Critical |
| 07 | Cache, Persist | High |
| 08 | Adaptive Query Execution (AQE) | High |
| 09 | Spark UI debugging | High |

## 5-Minute Revision Cheat Sheet

- **Driver:** JVM on master; builds DAG, schedules tasks, collects results.
- **Executor:** JVM on worker; runs tasks, stores cached data.
- **Job:** One action → one job.
- **Stage:** Bounded by shuffles; tasks in a stage are independent.
- **Task:** One partition on one executor.
- **Narrow:** map, filter — no shuffle. **Wide:** groupBy, join — shuffle.
- **repartition(n):** Shuffle. Use to increase partitions. **coalesce(n):** No shuffle. Use to reduce.
- **Broadcast join:** Small table → all executors. **Sort-merge:** Default for large joins.
- **Cache:** MEMORY_AND_DISK. **Persist:** Choose level.
- **AQE:** Coalesce, skew handling, DPP at runtime.
