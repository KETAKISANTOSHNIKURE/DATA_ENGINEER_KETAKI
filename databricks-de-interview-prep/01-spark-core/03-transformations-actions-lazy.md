# Transformations, Actions, Lazy Evaluation

## ✅ What you need to say in interview

- **Transformation:** Returns a **new DataFrame**; does **not execute** (e.g., `filter`, `select`, `join`, `groupBy`).
- **Action:** **Triggers execution** and returns a result to driver or writes data (e.g., `count`, `show`, `write`, `collect`).
- **Lazy evaluation:** Spark **defers execution** until an action. Builds optimized **logical plan** first.

## ⚙️ How it actually works

1. Transformations build a logical plan (DAG).
2. Catalyst optimizer optimizes the plan.
3. On first action, physical plan is generated and executed.
4. Results flow back to driver or to storage.

## ✅ When to use

- Explaining why a job "does nothing" until `show()` or `write`.
- Justifying combining transformations before actions (optimization).
- Debugging: logical plan vs actual execution.

## ❌ When to NEVER use

- Don't call `count()` after every transformation "to check" — triggers full execution each time.
- Don't assume order of transformations doesn't matter for correctness (it can for some UDFs).

## 🚩 Common interview pitfalls

- Saying "lazy" means "slow" — it means deferred for optimization.
- Confusing `foreach` (action) with `map` (transformation).

## 💻 Working example (PySpark)

```python
# All lazy — nothing runs yet
df = spark.read.parquet("/data/")
df2 = df.filter("year = 2024").select("id", "amount").groupBy("id").sum("amount")

# Action — NOW execution happens
df2.write.parquet("/out/")   # or df2.count() or df2.show()
```

## ❔ Actual interview questions + ideal answers

**Q: What is lazy evaluation and why does Spark use it?**

- **Junior:** Spark waits until an action to run. It helps optimize.
- **Senior:** **Lazy evaluation** means transformations build a logical plan but don't execute. When an **action** runs, Catalyst can **optimize the entire plan**—e.g., predicate pushdown, projection pruning, combining filters. It also avoids redundant work if you reuse a cached DataFrame.

**Q: Is `count()` a transformation or action?**

- **Junior:** Action.
- **Senior:** **Action.** It triggers a full scan (or uses metadata when possible, e.g., Parquet row count) and returns a value to the driver. Use sparingly; prefer `limit(1).count()` for existence checks.

---

## 5-Minute Revision Cheat Sheet

- Transformation: returns DataFrame, no execution.
- Action: triggers execution, returns/writes.
- Lazy = deferred for optimization.
- `filter`, `select`, `join`, `groupBy` = transformation; `count`, `show`, `write`, `collect` = action.
