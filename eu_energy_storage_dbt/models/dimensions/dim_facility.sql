{{ config(materialized='table') }}

select
    facility_id,
    country,
    max_capacity_gwh,
    operator
from {{ ref('stg_facility_master') }}