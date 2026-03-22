# Job-Stage-Task

## ✅ What you need to say in interview

- **Job:** Triggered by a **single action** (e.g., `count()`, `write()`, `collect()`). One action = one job.
- **Stage:** A **set of tasks** that can run in parallel without a shuffle. Stages are **separated by shuffle boundaries**.
- **Task:** **One partition processed on one executor**. Smallest unit of work.

**Hierarchy:** Job → Stages (bounded by shuffles) → Tasks (one per partition per stage)

## ⚙️ How it actually works

1. Action triggers job submission.
2. DAG Scheduler analyzes DAG and splits into stages at shuffle boundaries.
3. Stages execute in topological order; within a stage, tasks run in parallel.
4. Shuffle write at end of stage; next stage does shuffle read.

## ✅ When to use

- Explaining why a job has multiple stages (shuffles).
- Debugging: identify which stage is slow.
- Optimizing: fewer stages = fewer shuffles.

## ❌ When to NEVER use

- Don't say "stage = one task" — stage has many tasks.
- Don't confuse job with application (application can have many jobs).

## 🚩 Common interview pitfalls

- Saying "task" when you mean "stage."
- Not knowing that shuffle creates a stage boundary.

## 💻 Working example (PySpark)

```python
df = spark.read.parquet("/data/")
df2 = df.groupBy("region").sum("sales")   # Shuffle here → stage boundary
df2.write.parquet("/out/")                # Action → 1 job, 2+ stages
# Stage 1: read + groupBy (shuffle write)
# Stage 2: shuffle read + write
```

## ❔ Actual interview questions + ideal answers

**Q: What is the relationship between job, stage, and task?**

- **Junior:** Job has stages, stages have tasks. Tasks do the actual work.
- **Senior:** **Job** is created per action. **Stage** is a set of transformations that don't require shuffle between them—shuffle creates a stage boundary. **Task** is one partition executed on one executor. A stage with 200 partitions spawns 200 tasks that run in parallel.

**Q: Why does my job have 3 stages?**

- **Junior:** Because there are shuffles.
- **Senior:** Each **shuffle** (e.g., `groupBy`, `join` without broadcast) creates a **stage boundary**. If you have two shuffles in the DAG, you get at least three stages: pre-shuffle, between shuffles, post-shuffle.

---

## 5-Minute Revision Cheat Sheet

- Job = 1 action.
- Stage = work between shuffles; shuffle = stage boundary.
- Task = 1 partition on 1 executor.
- Fewer shuffles → fewer stages → faster.
