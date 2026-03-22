# Medallion Architecture

## ✅ What you need to say in interview

- **Medallion:** Three layers—**Bronze** (raw), **Silver** (cleaned, deduped), **Gold** (aggregated, business-ready).
- **Bronze:** Raw ingestion, append-only, schema-on-read, immutable.
- **Silver:** Cleaned, typed, deduplicated, conformed. Typically Delta.
- **Gold:** Aggregations, dimensions, marts. Optimized for consumption.

## ⚙️ How it actually works

1. Raw data lands in Bronze (e.g., JSON, Parquet).
2. Silver: apply schema, validate, dedupe, merge with existing.
3. Gold: join Silver tables, aggregate, create marts.
4. Each layer can be incremental.

## ✅ When to use

- Standard design for lakehouse.
- Clear separation of concerns.
- Supports multiple consumers from same Bronze.

## ❌ When to NEVER use

- Don't put business logic in Bronze.
- Don't skip Silver for complex transformations—hard to debug.
- Don't create too many Gold marts without governance.

## 🚩 Common interview pitfalls

- Saying Bronze is "cleaned" (it's raw).
- Confusing Silver and Gold—Silver = cleansed rows; Gold = aggregated/dimensional.

## 💻 Working example (SQL + PySpark)

```python
# Bronze: raw
(spark.readStream.format("cloudFiles").option("cloudFiles.format", "json")
 .load("/raw/").writeStream.toTable("bronze_events"))

# Silver: clean, dedupe
# (see deduplication + MERGE)

# Gold: aggregate
spark.sql("""
  CREATE OR REPLACE TABLE gold_daily_sales AS
  SELECT date, region, sum(amount) as total
  FROM silver_orders
  GROUP BY date, region
""")
```

## ❔ Actual interview questions + ideal answers

**Q: What is the Medallion architecture?**

- **Junior:** Bronze, Silver, Gold layers. Raw, clean, aggregated.
- **Senior:** **Medallion** is a layered architecture: **Bronze** = raw, immutable, append-only ingestion. **Silver** = cleaned, typed, deduplicated, conformed schema. **Gold** = business-level aggregations, dimensions, marts. Enables incremental processing, reuse, and clear lineage. Databricks recommends it for lakehouse.

**Q: Why not just Bronze and Gold?**

- **Junior:** Silver adds a cleaning layer.
- **Senior:** **Silver** provides a **single source of truth** for cleansed data. Multiple Gold marts can consume from Silver without duplicating cleaning logic. Silver also enables **incremental processing** and **CDC**—Bronze is append-only; Silver handles merges. Skipping Silver means embedding cleanup in Gold, which becomes hard to maintain and replay.

---

## 5-Minute Revision Cheat Sheet

- Bronze: raw, append-only.
- Silver: cleaned, deduped, typed.
- Gold: aggregated, marts.
- Incremental at each layer.
