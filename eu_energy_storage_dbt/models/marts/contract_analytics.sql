{{ config(materialized='table') }}

with contract as (

    select
        contract_id,
        start_date,
        end_date,
        price_eur_per_mwh
    from {{ ref('dim_contract') }}

),

customer as (

    select
        customer_id,
        customer_name,
        contract_id,
        facility_id,
        credit_status,
        risk_rating,
        current_customer
    from {{ ref('dim_customer') }}

),

sales as (

    select
        customer_id,
        count(distinct booking_id) as total_bookings,
        sum(booked_capacity_mw) as total_booked_capacity_mw,
        sum(gas_volume_mwh) as total_gas_volume_mwh
    from {{ ref('fact_sales_operations') }}
    group by customer_id

)

select
    c.contract_id,
    cu.customer_id,
    cu.customer_name,
    cu.facility_id,
    cu.credit_status,
    cu.risk_rating,
    cu.current_customer,
    c.start_date,
    c.end_date,
    c.price_eur_per_mwh,

    datediff('day', current_date, c.end_date) as days_until_contract_end,

    coalesce(s.total_bookings, 0) as total_bookings,
    coalesce(s.total_booked_capacity_mw, 0) as total_booked_capacity_mw,
    coalesce(s.total_gas_volume_mwh, 0) as total_gas_volume_mwh,

    coalesce(s.total_gas_volume_mwh, 0) * c.price_eur_per_mwh as estimated_contract_value_eur,

    case
        when c.end_date < current_date then 'Expired'
        when datediff('day', current_date, c.end_date) <= 90 then 'Expiring Soon'
        else 'Active'
    end as contract_status_category

from contract c
left join customer cu
    on c.contract_id = cu.contract_id
left join sales s
    on cu.customer_id = s.customer_id