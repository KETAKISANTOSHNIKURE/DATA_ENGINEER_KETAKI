from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id="spark_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    run_spark = BashOperator(
        task_id="run_spark_job",
        bash_command="python /opt/project/src/etl_pipeline.py"
    )

    run_spark
