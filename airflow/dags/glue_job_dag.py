from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator


AWS_REGION = "us-east-1"


with DAG(
    dag_id="eu_energy_glue_orchestration",
    start_date=datetime(2026, 6, 7),
    schedule=None,
    catchup=False,
    tags=["eu-energy", "glue", "medallion"],
) as dag:

    start = EmptyOperator(task_id="start")

    raw_to_silver_risk_mgt = GlueJobOperator(
        task_id="raw_to_silver_risk_mgt",
        job_name="raw_to_silver_risk_mgt.py",
        region_name=AWS_REGION,
    )

    raw_to_silver_sales_dept = GlueJobOperator(
        task_id="raw_to_silver_sales_dept",
        job_name="raw_to_silver_sales_dept.py",
        region_name=AWS_REGION,
    )

    raw_to_silver_facilities = GlueJobOperator(
        task_id="raw_to_silver_facilities",
        job_name="raw_to_silver_facilities.py",
        region_name=AWS_REGION,
    )

    silver_to_gold_customer_master = GlueJobOperator(
        task_id="silver_to_gold_customer_master",
        job_name="silver_to_gold_customer_master",
        region_name=AWS_REGION,
    )

    silver_to_gold_facility_master = GlueJobOperator(
        task_id="silver_to_gold_facility_master",
        job_name="facility master",
        region_name=AWS_REGION,
    )

    silver_to_gold_sales_operations = GlueJobOperator(
        task_id="silver_to_gold_sales_operations",
        job_name="ales operations table",
        region_name=AWS_REGION,
    )

    silver_to_gold_contract_master = GlueJobOperator(
        task_id="silver_to_gold_contract_master",
        job_name="Contract Master Table",
        region_name=AWS_REGION,
    )

    end = EmptyOperator(task_id="end")


    start >> [
        raw_to_silver_risk_mgt,
        raw_to_silver_sales_dept,
        raw_to_silver_facilities,
    ]

    raw_to_silver_risk_mgt >> silver_to_gold_customer_master

    raw_to_silver_facilities >> silver_to_gold_facility_master

    raw_to_silver_sales_dept >> [
        silver_to_gold_sales_operations,
        silver_to_gold_contract_master,
    ]

    [
        silver_to_gold_customer_master,
        silver_to_gold_facility_master,
        silver_to_gold_sales_operations,
        silver_to_gold_contract_master,
    ] >> end