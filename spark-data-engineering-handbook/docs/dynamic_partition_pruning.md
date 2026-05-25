# Dynamic Partition Pruning (DPP)

## What is Dynamic Partition Pruning?

Dynamic Partition Pruning is a **query optimization technique** in Spark where the engine
skips reading unnecessary partitions at **runtime** based on filter conditions from a JOIN operation.

---

## Simple Analogy

```
Library with 12 shelves (one per month):

Without DPP → Search ALL 12 shelves
With DPP    → Know book is from March → go directly to shelf 3
```

---

## How It Works

### Without DPP
```
Large Fact Table (partitioned by date)
     ↓
Spark reads ALL partitions first
     ↓
Then applies filter after JOIN
     ↓
Very slow — reads unnecessary data ❌
```

### With DPP
```
Small Dimension Table
     ↓
Spark reads filter condition FIRST (e.g., only Jan 2024 dates)
     ↓
Reads ONLY matching partitions from Large Fact Table
     ↓
Much faster — skips irrelevant partitions ✅
```

---

## Code Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DPP_Example").getOrCreate()

# Fact table — partitioned by sale_date (millions of rows)
fact_sales = spark.table("fact_sales")

# Dimension table — small filter table
dim_date = spark.table("dim_date").filter("year = 2024")

# JOIN — DPP kicks in automatically!
# Spark sees dim_date filtered to 2024
# So it ONLY reads 2024 partitions from fact_sales
# Skips 2022 and 2023 partitions entirely!
result = fact_sales.join(dim_date, fact_sales.sale_date == dim_date.date_key)
result.show()
```

---

## Enable DPP in Spark

```python
# Enable Dynamic Partition Pruning (ON by default in Spark 3.x)
spark.conf.set("spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")

# Works best together with AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

---

## When DPP Works ✅

| Condition | Required |
|---|---|
| Table must be partitioned | ✅ Yes |
| One table must be small (dimension) | ✅ Yes |
| Join type: inner or left join | ✅ Yes |
| Filter on the small table | ✅ Yes |
| Spark version 3.0+ | ✅ Yes |

## When DPP Does NOT Work ❌

- Table is NOT partitioned
- Both tables are equally large
- Using full outer join
- Filter is on the large table directly (that is static pruning)

---

## DPP vs Static Partition Pruning

| | Static Pruning | Dynamic Pruning |
|---|---|---|
| When | Filter hardcoded | Filter from JOIN at runtime |
| Example | `WHERE date = '2024-01-01'` | Filter from dimension table |
| Spark decides | At parse time | At runtime |

```python
# Static Pruning — Spark knows at compile time
df.filter("sale_date = '2024-01-01'")

# Dynamic Pruning — Spark decides at RUNTIME
fact.join(dim.filter("year=2024"), "date_key")
```

---

## Related Concepts

| Concept | Description |
|---|---|
| AQE | Spark re-optimizes query plan at runtime |
| Broadcast Join | Small table sent to all executors — avoids shuffle |
| Predicate Pushdown | Filter pushed to data source level |
| Data Skipping | Delta Lake skips files based on min/max stats |

---

## Interview Answer

> "Dynamic Partition Pruning is a Spark optimization where instead of scanning all partitions
> of a large fact table, Spark first evaluates the filter from a smaller dimension table at
> runtime and reads only the relevant partitions. For example if I join a sales fact table
> partitioned by date with a date dimension filtered to 2024, Spark automatically skips 2022
> and 2023 partitions. This significantly reduces I/O and improves query performance.
> It is enabled by default in Spark 3.x and works best with AQE."
