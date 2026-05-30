{{ config(materialized='table') }}

select
    customer_id,
    customer_name,
    contract_id,
    facility_id,
    credit_status,
    credit_limit_eur,
    risk_rating,
    current_customer
from {{ ref('stg_customer_master') }}