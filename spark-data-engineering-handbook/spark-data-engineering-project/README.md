# Spark Data Engineering Project

This repository demonstrates a production-style data engineering pipeline using PySpark.

**Pipeline architecture:**

```
Kafka → Spark → Data Lake → Analytics
```

## Technologies

- **PySpark** – distributed data processing
- **Apache Spark** – cluster computing
- **Docker** – containerized Spark cluster
- **Apache Airflow** – pipeline orchestration
- **Parquet** – data lake storage format

## Project Structure

```
spark-data-engineering-project/
├── src/           → PySpark ETL code
├── data/          → sample dataset
├── docker/        → Spark cluster setup
├── airflow/       → pipeline orchestration
├── notebooks/     → analysis notebooks
└── requirements.txt
```

## Run the Project

**1. Start Spark cluster:**

```bash
docker-compose -f docker/docker-compose.yml up
```

**2. Run ETL job:**

```bash
python src/etl_pipeline.py
```

Output data will be written to: `data/output/`

## Example Transformation

**Input:**

| user_id | product_id | price | country |
|---------|------------|-------|---------|
| 1 | 100 | 120 | India |
| 2 | 200 | 80 | USA |

**Output (aggregated revenue):**

| country | revenue |
|---------|---------|
| India | 120 |
| USA | 80 |

This project demonstrates how distributed data pipelines are built with Spark.
