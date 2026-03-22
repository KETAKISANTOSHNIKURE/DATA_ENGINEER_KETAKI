# Photon Runtime

## ✅ What you need to say in interview

- **Photon:** Databricks **native vectorized engine** for Spark SQL and DataFrame. Drop-in replacement; **faster** for many workloads.
- **Benefits:** Vectorized execution, better codegen, optimized for modern CPUs. Up to **3–5× faster** for some queries.
- **When:** Enable on cluster (Photon worker nodes). Works with SQL, DataFrame, Delta. No code changes.
- **Limitations:** Some Spark features not yet supported; check docs. Typically SQL/DataFrame and Delta are well-supported.

## ⚙️ How it actually works

- Photon runs as alternative to standard Spark engine for supported ops.
- Vectorized: processes batches of rows; better CPU cache use.
- Falls back to Spark for unsupported ops.

## ✅ When to use

- Default for new clusters when available (cost permitting).
- SQL/analytics workloads.
- Delta reads/writes.
- When optimizing for performance.

## ❌ When to NEVER use

- Check compatibility for RDD, certain UDFs, or exotic features.
- Cost: Photon nodes may have different pricing.
- Don't assume all workloads benefit equally—benchmark.

## 🚩 Common interview pitfalls

- Saying Photon requires code changes (it doesn't).
- Not knowing it's Databricks-specific.
- Confusing with Delta/Spark—Photon is execution engine.

## 💻 Working example (SQL + PySpark)

```python
# Enable Photon: cluster config
# Databricks UI: Cluster → Advanced → Use Photon Acceleration
# Or: spark.databricks.photon.enabled = true (cluster config)
# No code changes—queries run on Photon when supported
spark.sql("SELECT * FROM huge_table WHERE date = '2024-01-01'").count()
```

## ❔ Actual interview questions + ideal answers

**Q: What is Photon?**

- **Junior:** Databricks' faster Spark engine.
- **Senior:** **Photon** is Databricks' **native vectorized execution engine** for Spark SQL and DataFrame. It's a **drop-in replacement**—no code changes. Uses vectorized processing and optimizations for modern CPUs. Can give **3–5× speedup** for analytics workloads. Enable on cluster (Photon worker nodes). Falls back to Spark for unsupported operations.

**Q: When would you use Photon?**

- **Junior:** When we need better performance on Databricks.
- **Senior:** For **SQL and DataFrame** workloads on Databricks—especially analytics, aggregations, Delta reads/writes. Enable by default for new clusters if budget allows. **Benchmark** for your workload—some benefit more than others. Check **compatibility** for RDD, custom UDFs, or rare features. No code change—transparent acceleration.

---

## 5-Minute Revision Cheat Sheet

- Photon = Databricks vectorized engine.
- Drop-in; no code change.
- 3–5× for many queries.
- Enable on cluster.
- SQL, DataFrame, Delta supported.
