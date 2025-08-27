from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from pathlib import Path
import os

PROJECT_DIR = str(Path(__file__).resolve().parents[2])
RAW = f"{PROJECT_DIR}/data/raw/yellow_tripdata_sample.csv"
OUT = f"{PROJECT_DIR}/data/curated/hourly_fares"
SPARK_APP = f"{PROJECT_DIR}/jobs/nyc_batch.py"

# Make sure SPARK_HOME & JAVA_HOME are inherited; fallback defaults (Homebrew paths) below
ENV = {
    "SPARK_HOME": os.environ.get("SPARK_HOME", "/opt/homebrew/opt/apache-spark/libexec"),
    "JAVA_HOME": os.environ.get("JAVA_HOME", "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"),
    "PATH": os.environ.get("PATH", ""),  # include shell PATH
    "GOOGLE_CLOUD_PROJECT": 'gcp-big-self-009',
    "GOOGLE_APPLICATION_CREDENTIALS": f'"{PROJECT_DIR}/airflow_home/secret/gcp-big-self-009-8a0269bcd9a5.json"'
}
default_args = {
    "owner": "johny",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="nyc_batch_pipeline",
    start_date=datetime(2025, 8, 1),
    schedule=None,           # trigger manually to start
    catchup=False,
    default_args=default_args,
    tags=["spark", "batch"],
) as dag:
       
        # optional: a quick check step
    check_input = BashOperator(
        task_id="check_input",
        bash_command=f'[[ -f "{RAW}" ]] && echo "Found input file" || (echo "Missing input CSV"; exit 1)',
    )

    spark_transform = BashOperator(
        task_id = "spark_transform",
        bash_command=(f'{ENV["SPARK_HOME"]}/bin/spark-submit ' \
        '--master local[*] ' \
        f'"{SPARK_APP}" "{RAW}" "{OUT}"'
    ),
    env = ENV )

    show_output = BashOperator(
        task_id="show_output",
        bash_command=f'ls -lah "{OUT}" && echo "Done."',
    )

    check_input>>spark_transform>>show_output