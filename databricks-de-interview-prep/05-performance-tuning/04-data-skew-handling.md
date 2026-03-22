# Data Skew Handling

## ✅ What you need to say in interview

- **Skew:** Uneven data distribution—some partitions have **much more** data than others. One task does 10× the work.
- **Causes:** Skewed join keys (e.g., null, popular customer_id), skewed partition keys.
- **Solutions:** (1) **Salting**—add random suffix to key, distribute, then aggregate. (2) **AQE skew join**—Spark splits skewed partitions at runtime. (3) **Split skewed keys**—handle hot keys separately. (4) **Filter nulls** before join.

## ⚙️ How it actually works

1. Salting: `key_salt = key || "_" || rand(0, N)`; join on key_salt; aggregate back by key.
2. AQE: detects skew from stats; splits large partitions.
3. Separate handling: process hot keys in a separate path with more parallelism.

## ✅ When to use

- When Spark UI shows one task much slower than others.
- When join/groupBy key is skewed (e.g., null, default values).
- AQE skew join (default on Spark 3.x).

## ❌ When to NEVER use

- Don't salt without understanding—adds complexity, extra shuffle.
- Don't ignore skew—one straggler delays the whole stage.
- AQE doesn't always fix severe skew—manual salting may be needed.

## 🚩 Common interview pitfalls

- Not recognizing skew (check task duration distribution).
- Over-salting—too many salt values = many small partitions.
- Confusing skew with too few partitions.

## 💻 Working example (SQL + PySpark)

```python
# Salting
from pyspark.sql.functions import rand, concat, col
df1_salted = df1.withColumn("salt", (rand() * 10).cast("int")).withColumn("key_salt", concat(col("key"), lit("_"), col("salt")))
df2_salted = df2.withColumn("salt", (rand() * 10).cast("int")).withColumn("key_salt", concat(col("key"), lit("_"), col("salt")))
joined = df1_salted.join(df2_salted, "key_salt").drop("salt", "key_salt")
result = joined.groupBy("key").agg(...)  # aggregate back
```

## ❔ Actual interview questions + ideal answers

**Q: How do you handle data skew in Spark?**

- **Junior:** Use salting or AQE skew join.
- **Senior:** (1) **AQE skew join** (enabled by default)—splits skewed partitions at runtime. (2) **Salting:** add random suffix to key, repartition, join, then aggregate—spreads hot keys. (3) **Filter** skewed values (e.g., null) and handle separately. (4) **Split** hot keys into separate processing path. Diagnose via Spark UI—task duration distribution; one task 10× others = skew.

**Q: What is salting and when do you use it?**

- **Junior:** Add random value to key to spread data. Use when one key has too much data.
- **Senior:** **Salting** adds a random component to the join key (e.g., `key || "_" || rand(0, N)`) so that hot keys are **spread across multiple partitions**. After join, aggregate back by original key. Use when **AQE skew join** isn't sufficient—e.g., extreme skew. Trade-off: extra shuffle, more complexity. Choose N (salt buckets) to balance—too many = many small partitions; too few = still skewed.

---

## 5-Minute Revision Cheat Sheet

- Skew = uneven partitions; one task slow.
- AQE skew join (default).
- Salting for extreme skew.
- Filter nulls/special keys.
