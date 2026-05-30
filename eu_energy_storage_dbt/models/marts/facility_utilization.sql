{{ config(materialized='table') }}

with facility as (

    select
        facility_id,
        country,
        max_capacity_gwh,
        operator
    from {{ ref('dim_facility') }}

),

sales as (

    select
        facility_id,
        count(distinct booking_id) as total_bookings,
        sum(booked_capacity_mw) as total_booked_capacity_mw,
        sum(gas_volume_mwh) as total_gas_volume_mwh,
        avg(ttf_price_eur_mwh) as avg_ttf_price_eur_mwh,
        avg(nbp_price_eur_mwh) as avg_nbp_price_eur_mwh
    from {{ ref('fact_sales_operations') }}
    group by facility_id

)

select
    f.facility_id,
    f.country,
    f.operator,
    f.max_capacity_gwh,
    coalesce(s.total_bookings, 0) as total_bookings,
    coalesce(s.total_booked_capacity_mw, 0) as total_booked_capacity_mw,
    coalesce(s.total_gas_volume_mwh, 0) as total_gas_volume_mwh,
    s.avg_ttf_price_eur_mwh,
    s.avg_nbp_price_eur_mwh,

    case
        when f.max_capacity_gwh is null or f.max_capacity_gwh = 0 then null
        else round((s.total_gas_volume_mwh / (f.max_capacity_gwh * 1000)) * 100, 2)
    end as utilization_pct

from facility f
left join sales s
    on f.facility_id = s.facility_id