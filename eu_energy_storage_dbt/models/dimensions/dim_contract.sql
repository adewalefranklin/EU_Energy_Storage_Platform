{{ config(materialized='table') }}

select
    contract_id,
    start_date,
    end_date,
    price_eur_per_mwh
from {{ ref('stg_contract_master') }}