from datetime import datetime, timezone
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from eu_energy_pipeline.config import Config
from eu_energy_pipeline.extract import Extractor
from eu_energy_pipeline.load import S3Loader

dag = DAG(
    dag_id="eu_energy_platform_elt",
    start_date=datetime(2026, 5, 26),
    schedule=None,
    catchup=False,
    tags=["energy", "elt", "aws", "s3"],
)


def fetch_load_storage_agsi_data():
    endpoint = "storage"

    params = {
        "country": "AT",
        "from": "2024-01-01",
        "to": "2024-01-31",
    }

    ingestion_date = datetime.now(timezone.utc).date().isoformat()

    extractor = Extractor()

    data = extractor.fetch_data(
        endpoint=endpoint,
        params=params,
    )

    loader = S3Loader(
        aws_access_key_id=Config.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=Config.get("AWS_SECRET_ACCESS_KEY"),
        aws_region=Config.get("AWS_REGION"),
        prefix=Config.get("PREFIX"),
        aws_bucket_name=Config.get("AWS_BUCKET_NAME"),
    )

    s3_key = loader.s3_uploader(
        data=data,
        endpoint=endpoint,
        ingestion_date=ingestion_date,
    )

    return s3_key


def fetch_load_facility_agsi_data():
    endpoint = "facility"

    params = {
        "country": "AT",
        "from": "2024-01-01",
        "to": "2024-01-31",
    }

    ingestion_date = datetime.now(timezone.utc).date().isoformat()

    extractor = Extractor()

    data = extractor.fetch_data(
        endpoint=endpoint,
        params=params,
    )

    loader = S3Loader(
        aws_access_key_id=Config.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=Config.get("AWS_SECRET_ACCESS_KEY"),
        aws_region=Config.get("AWS_REGION"),
        prefix=Config.get("PREFIX"),
        aws_bucket_name=Config.get("AWS_BUCKET_NAME"),
    )

    s3_key = loader.s3_uploader(
        data=data,
        endpoint=endpoint,
        ingestion_date=ingestion_date,
    )

    return s3_key


start = EmptyOperator(task_id="start")

extract_load_storage_raw_to_s3 = PythonOperator(
    task_id="fetch_load_storage_agsi_data_to_s3",
    python_callable=fetch_load_storage_agsi_data,
    dag=dag,
)

extract_facility_load_raw_to_s3 = PythonOperator(
    task_id="fetch_load_facility_agsi_data_to_s3",
    python_callable=fetch_load_facility_agsi_data,
    dag=dag,
)

end = EmptyOperator(task_id="end")

start >> extract_load_storage_raw_to_s3 >> extract_facility_load_raw_to_s3 >> end
