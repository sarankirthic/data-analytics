from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path

from ingestion.fetch_news import put_newsapi
from processing.process_news import get_latest_raw_directory, find_json_file, process_news
from storage.upload_s3 import upload_to_s3
from config import Config

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 9, 21),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define base directory for data storage
BASE_DIR = Path(Config.BASE_DIR)


def ingest(**kwargs):
    raw_directory = BASE_DIR / 'data' / 'raw' / datetime.now().strftime("%Y%m%d%H%M%S")
    raw_directory.mkdir(parents=True, exist_ok=True)
    put_newsapi(raw_directory)


def process(**kwargs):
    latest_dir = get_latest_raw_directory(BASE_DIR)
    json_file = find_json_file(latest_dir)
    df_processed = process_news(json_file)
    processed_dir = BASE_DIR / 'data' / 'processed' / latest_dir.name
    processed_dir.mkdir(parents=True, exist_ok=True)
    df_processed.to_csv(processed_dir / "processed_news.csv", index=False)


def upload(**kwargs):
    latest_dir = get_latest_raw_directory(BASE_DIR)
    processed_dir = BASE_DIR / 'data' / 'processed' / latest_dir.name
    upload_to_s3(str(processed_dir / "processed_news.csv"), Config.AWS_S3_BUCKET_NAME)


with DAG(
    "news_data_pipeline",
    default_args=default_args,
    # schedule_interval="@hourly",
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id="ingest_news", python_callable=ingest)
    t2 = PythonOperator(task_id="process_news", python_callable=process)
    t3 = PythonOperator(task_id="upload_news", python_callable=upload)

    t1 >> t2 >> t3
