# Schema Drift Handling in PySpark Pipelines

## What is Schema Drift?

> Schema drift happens when the **source file or table structure changes unexpectedly**
> — new column added, column renamed, data type changed, column removed.

```
Common causes:
- Source team adds new column without notice
- Column renamed (e.g. amount → transaction_amount)
- Data type changed (string → integer)
- Column removed from source
```

---

## Why It Is a Problem

```
Pipeline reads CSV with schema: [user_id, amount, date]
Source team renames: amount → transaction_amount

Pipeline breaks with:
AnalysisException: Column 'amount' not found

OR worse — loads NULL values silently!
```

---

## Approach 1 — Delta Lake mergeSchema (Best for New Columns)

```python
# Automatically accept new columns added to source
df.write \
    .format("delta") \
    .option("mergeSchema", "true") \
    .mode("append") \
    .save("/delta/transactions")

# Delta Lake automatically adds new columns to target table
# Existing columns unchanged ✅
```

---

## Approach 2 — Detect Schema Changes Before Loading

```python
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

def detect_schema_drift(new_df: DataFrame, expected_schema: StructType):
    """
    Compares incoming data schema against expected schema.
    Raises exception if critical columns are missing.
    Logs warning if new columns are added.
    """
    new_cols = set(new_df.columns)
    expected_cols = set([f.name for f in expected_schema.fields])

    # New columns added in source
    added_cols = new_cols - expected_cols

    # Columns removed/renamed in source
    removed_cols = expected_cols - new_cols

    if added_cols:
        print(f"WARNING: New columns detected: {added_cols}")
        # Log to monitoring table or send alert email
        log_schema_change("ADDED", added_cols)

    if removed_cols:
        print(f"CRITICAL: Columns missing: {removed_cols}")
        # Stop pipeline — this is a critical failure
        send_alert(f"Schema drift! Missing columns: {removed_cols}")
        raise Exception(f"Pipeline stopped: Missing columns {removed_cols}")

    return True


def log_schema_change(change_type, columns):
    # Log to audit table
    print(f"Schema change logged: {change_type} - {columns}")


def send_alert(message):
    # Send email/Slack alert
    print(f"ALERT SENT: {message}")


# Usage in pipeline
expected_schema = spark.table("target_table").schema
new_data = spark.read.csv("s3://bucket/new_file.csv", header=True)

detect_schema_drift(new_data, expected_schema)
# Only proceeds if schema is valid
```

---

## Approach 3 — Read with Enforced Schema

```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Define expected schema explicitly
expected_schema = StructType([
    StructField("user_id",    StringType(), True),
    StructField("amount",     DoubleType(), True),
    StructField("txn_date",   StringType(), True)
])

# Read with enforced schema
# Extra columns in CSV → ignored
# Missing columns → error raised
df = spark.read \
    .schema(expected_schema) \
    .option("mode", "PERMISSIVE") \
    .csv("s3://bucket/data.csv")
```

---

## Approach 4 — Handle Multiple Date Formats (Real Production Fix)

```python
# Problem: Source file had mixed date formats
# Some rows: DD-MM-YYYY, others: YYYY-MM-DD

from pyspark.sql.functions import to_date, coalesce

# Try multiple formats — use whichever works
df = df.withColumn("transaction_date",
    coalesce(
        to_date(col("transaction_date"), "yyyy-MM-dd"),
        to_date(col("transaction_date"), "dd-MM-yyyy"),
        to_date(col("transaction_date"), "MM/dd/yyyy")
    )
)

# Flag rows where date couldn't be parsed
df = df.withColumn("date_parse_error",
    col("transaction_date").isNull()
)

# Count bad rows
bad_count = df.filter(col("date_parse_error")).count()
print(f"Rows with date parse errors: {bad_count}")
```

---

## Approach 5 — Add Schema Validation as DAG Task

```python
# In AirFlow — add schema check as first task
from airflow import DAG
from airflow.operators.python import PythonOperator

def validate_schema_task():
    new_df = spark.read.csv("s3://bucket/latest/", header=True)
    expected = spark.table("target_table").schema
    detect_schema_drift(new_df, expected)
    print("Schema validation passed ✅")

with DAG("migration_dag", ...) as dag:

    schema_check = PythonOperator(
        task_id="validate_schema",
        python_callable=validate_schema_task
    )

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_fn
    )

    # Schema check MUST pass before extraction
    schema_check >> extract >> transform >> load
```

---

## Production Scenarios

### ✅ Positive — Delta mergeSchema saved the pipeline
```
Source team added 2 new columns to CSV without notice.
Because we used Delta Lake with mergeSchema=true,
new columns were automatically added to Delta table.
No pipeline failure — just a notification about new columns.
```

### ❌ Negative — Silent NULL loading (Lesson learned)
```
Source renamed 'amount' to 'transaction_amount' silently.
Pipeline loaded NULL values for amount column.
Only caught during business reporting next morning!

Fix implemented:
→ Added schema drift detection as first DAG task
→ Compares incoming vs expected schema
→ Immediately alerts team if any column missing or renamed
→ Pipeline stops before loading bad data
```

---

## Schema Drift Detection Summary

| Scenario | Approach | Action |
|---|---|---|
| New column added | mergeSchema or detect | Log warning, continue |
| Column removed | Schema validation | Stop pipeline, alert |
| Column renamed | Schema validation | Stop pipeline, alert |
| Data type changed | Enforced schema | Error or cast |
| Mixed date formats | coalesce(to_date) | Parse with fallback |

---

## Interview Answer

> "Schema drift is one of the most common real-world challenges. We handle it at multiple
> levels. First we use Delta Lake with mergeSchema=true which automatically accepts new
> columns without pipeline failure. Second we have a schema drift detection function that
> runs as the first task in our AirFlow DAG — it compares incoming schema against expected
> and immediately alerts the team if any column is missing or renamed. We learned this the
> hard way when a column was renamed silently and we loaded NULL values for an entire day
> before business reported the issue. After that we added automated schema validation that
> stops the pipeline before any bad data reaches the warehouse."
