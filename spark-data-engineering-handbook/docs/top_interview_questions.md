# Spark & Data Engineering — Top Interview Questions

## Based on 2 Years Experience Level

---

## PySpark Questions

### Q1: What is the difference between repartition() and coalesce()?

> repartition does a full shuffle and can increase or decrease partitions with even
> distribution. coalesce only decreases partitions by merging locally without a shuffle —
> faster but may produce uneven partitions. Use repartition before large joins.
> Use coalesce after filtering or before writing output.

---

### Q2: When to use withColumn and when not to?

> Use withColumn for 1-2 column transformations. Never use it inside a loop or for
> many columns — each call adds a new query plan node causing performance issues.
> For multiple columns use select() with all transformations in one call.

---

### Q3: What is Dynamic Partition Pruning?

> DPP is a Spark optimization where the engine skips reading unnecessary partitions
> at runtime based on filters from a join's dimension table. For example joining a
> fact table partitioned by date with a dimension filtered to 2024 — Spark only reads
> 2024 partitions. Enabled by default in Spark 3.x, works best with AQE.

---

### Q4: How do you fix OOM errors in Spark?

> First check if driver or executor OOM. For executor OOM check Spark UI Tasks tab
> for data skew — one task with far more data than others. Fix with broadcast join
> for small tables, salting for skewed keys, or enable AQE skewJoin. Also check
> GC time in Executors tab — above 10% means memory pressure.

```python
# Key fixes:
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
result = large_df.join(broadcast(small_df), "key")
```

---

### Q5: What is spark.sql.shuffle.partitions?

> Controls how many partitions are created after shuffle operations like groupBy and join.
> Default is 200. For small data with 40 cores, set it to 40 — one partition per core.
> Target 100-200MB per partition. Best practice: enable AQE to auto-tune.

---

### Q6: What is the difference between map() and flatMap()?

```python
# map() — one input → one output
rdd.map(lambda x: x * 2)
# [1,2,3] → [2,4,6]

# flatMap() — one input → multiple outputs (flattens)
rdd.flatMap(lambda x: [x, x*2])
# [1,2,3] → [1,2,2,4,3,6]
```

---

### Q7: What are transformations vs actions?

```
Transformations — lazy, build query plan:
filter(), select(), withColumn(), groupBy(), join()

Actions — trigger actual execution:
show(), count(), collect(), write(), take()

Spark builds DAG of transformations
Only executes when action is called
```

---

## Spark Architecture Questions

### Q8: Difference between Worker Node and Executor?

> Worker Node is the physical/virtual machine — the infrastructure.
> Executor is a JVM process running ON the worker node — does actual computation.
> One worker can have multiple executors. Each executor has cores and memory.
> Driver communicates with executors to send tasks and collect results.

---

### Q9: What is a core in Spark?

> A core is the fundamental computing unit — executes one task at a time.
> 4 cores per executor = 4 tasks run simultaneously per executor.
> Total parallelism = total executors × cores per executor.
> Best practice: 4-5 cores per executor for optimal HDFS throughput.

---

### Q10: What is AQE (Adaptive Query Execution)?

> AQE re-optimizes the query plan at runtime based on actual data statistics.
> It can auto-coalesce shuffle partitions, handle skew joins, and convert
> sort-merge joins to broadcast joins dynamically.

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

---

## Data Engineering Questions

### Q11: Describe your end-to-end pipeline

> Our pipeline has two platforms. On the Databricks side, data from S3, Kafka, and
> DBX catalog flows through Raw → Work → Conformed → Published zones using PySpark
> and Delta Lake. Unity Catalog manages governance. On the Teradata side, data from
> Mainframe DB2 and VSAM files flows through Landing → Staging → Base → Eval zones.
> Both platforms synchronized via JDBC and Teradata NOS. AirFlow orchestrates all jobs.
> CI/CD through GitHub and Cloudbees.

---

### Q12: How do you handle schema drift?

> Multiple approaches: Delta Lake mergeSchema for new columns, schema drift detection
> function as first AirFlow DAG task that compares incoming vs expected schema and stops
> pipeline if critical columns missing, and coalesce(to_date) for mixed date formats.

---

### Q13: How do you debug a failed production job?

> Check AirFlow UI for failed task. Open Spark UI — Jobs tab for failed stage,
> Stages tab for shuffle sizes, Tasks tab for skew (one task much longer than others),
> Executors tab for GC time. SQL tab for query plan issues. Then fix root cause,
> test with sample data, rerun from failed task only, communicate to team.

---

### Q14: What is the difference between ETL and ELT?

```
ETL (Extract Transform Load):
- Transform data BEFORE loading to warehouse
- Used with traditional data warehouses
- Example: Transform in Spark → load to Teradata

ELT (Extract Load Transform):
- Load raw data FIRST then transform inside warehouse
- Used with modern cloud warehouses (Snowflake, BigQuery, Databricks)
- Example: Load to Delta Lake → transform with SQL/Spark
- More flexible — raw data preserved
```

---

### Q15: What is Medallion Architecture?

```
Bronze Layer (Raw Zone):
→ Raw data as-is from sources
→ No transformation
→ Preserve original data

Silver Layer (Refined):
→ Cleaned, validated, deduplicated
→ Applied business rules
→ Joined with reference data

Gold Layer (Business Ready):
→ Aggregated, summarized
→ Ready for analytics and reporting
→ Business-specific data products
```

---

## SQL Questions

### Q16: Find second highest salary per department handling single employee

```sql
WITH ranked AS (
    SELECT
        department,
        employee_name,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS rnk
    FROM employees
)
SELECT department, employee_name, salary
FROM ranked
WHERE rnk = 2;
-- Departments with only 1 employee simply won't appear ✅
```

---

### Q17: Difference between RANK, DENSE_RANK, ROW_NUMBER?

```sql
-- Data: salaries [100, 100, 90, 80]

ROW_NUMBER():  1, 2, 3, 4  (always unique, no gaps)
RANK():        1, 1, 3, 4  (ties same rank, gap after tie)
DENSE_RANK():  1, 1, 2, 3  (ties same rank, NO gap)
```

---

### Q18: What is a CTE and when to use it?

```sql
-- CTE = Common Table Expression
-- Use for: readability, reusing subquery, recursive queries

WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', sale_date) AS month,
        SUM(amount) AS total
    FROM sales
    GROUP BY 1
)
SELECT month, total,
       LAG(total) OVER (ORDER BY month) AS prev_month
FROM monthly_sales;
```

---

## Behavioral Questions

### Q19: Describe a pipeline failure and how you fixed it

> Our 1 AM migration job failed with OOM. AirFlow alert woke me.
> Checked AirFlow UI — PySpark task failed. Opened Spark UI — Task 67
> had 45M records vs 200K in others — data skew on country_code join key.
> Fixed with broadcast join and AQE. Tested with 1000 records sample first.
> Reran from failed task only — not from start. Job completed by 4 AM.
> Next morning added schema drift detection and skew monitoring as permanent fix.

---

### Q20: Why migrate from Teradata to Databricks/Delta Lake?

> Cost: Teradata licensing is very expensive vs cloud object storage.
> Scalability: Databricks auto-scales, Teradata has fixed capacity.
> Open format: Delta Lake uses open Parquet format, no vendor lock-in.
> Features: Time travel, MERGE, schema evolution, streaming support.
> Integration: Better with modern cloud tools, ML, BI platforms.
> Performance: Spark distributed processing handles petabyte scale.
