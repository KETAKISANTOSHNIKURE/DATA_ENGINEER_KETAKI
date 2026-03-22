# Adaptive Query Execution (AQE)

## ✅ What you need to say in interview

- **AQE:** Runtime optimizations applied **after** initial execution starts, using **actual statistics**.
- **Three features:** (1) **Coalesce partitions** — merge small partitions. (2) **Skew join** — split skewed partitions. (3) **Dynamic partition pruning (DPP)** — skip unnecessary partitions based on runtime filters.

## ⚙️ How it actually works

1. Spark runs initial stages and collects statistics (partition sizes, etc.).
2. Before later stages, AQE can: merge small partitions (fewer tasks), split skewed partitions (more parallelism), prune partitions using filter values.
3. Enabled by default in Spark 3.x (`spark.sql.adaptive.enabled = true`).

## ✅ When to use

- Default on Spark 3.x—usually leave enabled.
- Especially helpful for: dynamic partition pruning (star schema), skew, many small partitions.

## ❌ When to NEVER use

- Rarely disable; only if AQE causes unexpected plan changes.
- Don't rely solely on AQE—still optimize skew and partitioning when you know the data.

## 🚩 Common interview pitfalls

- Saying AQE optimizes at compile time (it's **runtime**).
- Not knowing the three features: coalesce, skew, DPP.
- Confusing DPP with predicate pushdown (both reduce scans; DPP uses runtime filter values).

## 💻 Working example (PySpark)

```python
# AQE is on by default in Spark 3.x
spark.conf.get("spark.sql.adaptive.enabled")  # true

# Coalesce small partitions
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Skew join
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Dynamic partition pruning (e.g., fact JOIN dimension filtered)
# SELECT f.* FROM fact f JOIN dim d ON f.dim_id = d.id WHERE d.region = 'US'
# AQE can prune fact partitions using d.region filter
```

## ❔ Actual interview questions + ideal answers

**Q: What is AQE and how does it help?**

- **Junior:** AQE optimizes queries at runtime. It helps with skew and partitions.
- **Senior:** **Adaptive Query Execution** applies **runtime optimizations** using actual data statistics. Key features: (1) **Coalesce partitions**—merge small partitions after shuffle to avoid many tiny tasks. (2) **Skew join**—split partitions that have much more data than others to balance load. (3) **Dynamic partition pruning**—use filter values from dimension tables to skip fact partitions at runtime. It's enabled by default in Spark 3.x.

**Q: How is DPP different from predicate pushdown?**

- **Junior:** Both reduce data. DPP is at runtime.
- **Senior:** **Predicate pushdown** pushes filters to the data source at **plan time**—e.g., Parquet file/row-group pruning. **DPP** uses **runtime values**—e.g., from a dimension filter in a join—to determine which partitions of a fact table to scan. Both reduce I/O; DPP is especially useful in star schemas with filtered dimension joins.

---

## 5-Minute Revision Cheat Sheet

- AQE = runtime optimization using actual stats.
- Coalesce partitions, skew join, DPP.
- Default on in Spark 3.x.
- DPP uses runtime filter values to skip partitions.
