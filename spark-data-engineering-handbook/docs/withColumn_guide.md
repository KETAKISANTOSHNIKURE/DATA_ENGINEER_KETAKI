# withColumn in PySpark — When to Use and When NOT to Use

## What is withColumn?

`withColumn` is a PySpark DataFrame transformation used to **add a new column** or **modify an existing column**.

```python
# Syntax
df.withColumn("new_col_name", expression)
```

---

## ✅ WHEN TO USE withColumn

### 1. Adding a Single New Derived Column
```python
from pyspark.sql.functions import col, lit, current_timestamp, upper, round

# Add derived column
df = df.withColumn("tax_amount", col("price") * 0.18)

# Add constant column
df = df.withColumn("country", lit("India"))

# Add timestamp
df = df.withColumn("load_date", current_timestamp())
```

### 2. Modifying / Transforming Existing Column
```python
# Convert to uppercase
df = df.withColumn("name", upper(col("name")))

# Cast data type
df = df.withColumn("age", col("age").cast("integer"))

# Round decimal
df = df.withColumn("salary", round(col("salary"), 2))
```

### 3. Conditional Logic
```python
from pyspark.sql.functions import when

df = df.withColumn("grade",
    when(col("marks") >= 90, "A")
    .when(col("marks") >= 70, "B")
    .when(col("marks") >= 50, "C")
    .otherwise("F")
)
```

### 4. Date Extraction
```python
from pyspark.sql.functions import year, month, dayofmonth

# Extract year from date column
year_df = df.withColumn("jyear", year(col("jdate")))

# Extract month
df = df.withColumn("jmonth", month(col("jdate")))

# Extract day
df = df.withColumn("jday", dayofmonth(col("jdate")))
```

### 5. Handling Nulls
```python
df = df.withColumn("city",
    when(col("city").isNull(), lit("Unknown"))
    .otherwise(col("city")))
```

---

## ❌ WHEN NOT TO USE withColumn

### ❌ 1. Adding Multiple Columns in a Loop — BIG PERFORMANCE ISSUE!

```python
# ❌ BAD — Never do this!
columns = ["col1", "col2", "col3", "col4", "col5"]

for c in columns:
    df = df.withColumn(c, lit(None))

# WHY BAD?
# Every withColumn call creates a NEW query plan node
# 50 withColumns = 50 nested query plans
# Spark optimizer struggles → very slow!
```

```python
# ✅ GOOD — Use select instead
df = df.select(
    "*",
    lit(None).alias("col1"),
    lit(None).alias("col2"),
    lit(None).alias("col3"),
)
# Single query plan → much faster!
```

### ❌ 2. When Adding Many Columns at Once

```python
# ❌ BAD — 5 separate query plan nodes
df = df.withColumn("tax", col("price") * 0.18) \
       .withColumn("discount", col("price") * 0.05) \
       .withColumn("final_price", col("price") * 0.95) \
       .withColumn("category", upper(col("category"))) \
       .withColumn("load_date", current_timestamp())

# ✅ GOOD — Single query plan node
df = df.select(
    "*",
    (col("price") * 0.18).alias("tax"),
    (col("price") * 0.05).alias("discount"),
    (col("price") * 0.95).alias("final_price"),
    upper(col("category")).alias("category"),
    current_timestamp().alias("load_date")
)
```

### ❌ 3. Just Renaming a Column

```python
# ❌ BAD
df = df.withColumn("customer_name", col("cust_nm")).drop("cust_nm")

# ✅ GOOD
df = df.withColumnRenamed("cust_nm", "customer_name")
```

### ❌ 4. Just Dropping a Column

```python
# ❌ BAD — using withColumn to nullify
# ✅ GOOD
df = df.drop("unwanted_column")
```

---

## Quick Decision Guide

```
Adding/modifying columns?
│
├── 1-2 columns?          → ✅ withColumn
├── 3+ columns?           → ✅ select()
├── Inside a loop?        → ❌ NEVER withColumn → use select()
├── Just renaming?        → ✅ withColumnRenamed()
└── Just dropping?        → ✅ drop()
```

---

## Summary Table

| Scenario | Best Approach |
|---|---|
| Add 1-2 new columns | `withColumn` ✅ |
| Add 3+ columns | `select` ✅ |
| Add columns in a loop | `select` ✅ Never `withColumn` |
| Rename column | `withColumnRenamed` ✅ |
| Drop column | `drop()` ✅ |
| SQL-style expression | `selectExpr` ✅ |
| Conditional logic | `withColumn` + `when` ✅ |

---

## Interview Answer

> "I use withColumn when adding or transforming one or two columns. I avoid it inside loops
> or for multiple columns because each withColumn call adds a new node to the query plan,
> causing performance degradation. For multiple columns I prefer select() with all
> transformations in a single call — one query plan node, significantly better performance."
