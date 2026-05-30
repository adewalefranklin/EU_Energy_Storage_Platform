{{ config(materialized='table') }}

select
    booking_id,
    customer_id,
    facility_id,
    booking_date,
    booked_capacity_mw,
    gas_volume_mwh,
    nomination_status,
    gas_price_date,
    ttf_price_eur_mwh,
    nbp_price_eur_mwh
from {{ ref('stg_sales_operations') }}