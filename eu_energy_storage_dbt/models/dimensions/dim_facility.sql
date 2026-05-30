{{ config(materialized='table') }}

select distinct
    facility_id,
    country,
    max_capacity_gwh,
    operator
from {{ ref('stg_facility_master') }}