from datetime import datetime, timezone

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from eu_energy_pipeline.pipeline import AgsiPipeline


DEFAULT_PARAMS = {
    "limit": 300,
}


def run_agsi_pipeline(endpoint: str) -> None:
    ingestion_date = datetime.now(timezone.utc).isoformat()

    pipeline = AgsiPipeline()

    pipeline.run(
        endpoint=endpoint,
        params=DEFAULT_PARAMS,
        ingestion_date=ingestion_date,
    )


with DAG(
    dag_id="extract_load",
    start_date=datetime(2026, 6, 7),
    schedule=None,
    catchup=False,
    tags=["eu-energy", "agsi", "api", "s3"],
) as dag:

    start = EmptyOperator(task_id="start")

    extract_load_storage = PythonOperator(
        task_id="extract_load_storage",
        python_callable=run_agsi_pipeline,
        op_kwargs={"endpoint": "storage"},
    )

    extract_load_facilities = PythonOperator(
        task_id="extract_load_facilities",
        python_callable=run_agsi_pipeline,
        op_kwargs={"endpoint": "facilities"},
    )

    end = EmptyOperator(task_id="end")

    start >> [
        extract_load_storage,
        extract_load_facilities,
    ] >> end