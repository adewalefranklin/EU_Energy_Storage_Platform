{{ config(materialized='table') }}

with customer as (

    select
        customer_id,
        customer_name,
        contract_id,
        facility_id,
        credit_status,
        credit_limit_eur,
        risk_rating,
        current_customer
    from {{ ref('dim_customer') }}

),

sales as (

    select
        customer_id,
        count(distinct booking_id) as total_bookings,
        sum(booked_capacity_mw) as total_booked_capacity_mw,
        sum(gas_volume_mwh) as total_gas_volume_mwh,
        avg(ttf_price_eur_mwh) as avg_ttf_price_eur_mwh,
        avg(nbp_price_eur_mwh) as avg_nbp_price_eur_mwh
    from {{ ref('fact_sales_operations') }}
    group by customer_id

),

contract as (

    select
        contract_id,
        start_date,
        end_date,
        price_eur_per_mwh
    from {{ ref('dim_contract') }}

)

select
    c.customer_id,
    c.customer_name,
    c.contract_id,
    c.facility_id,
    c.credit_status,
    c.credit_limit_eur,
    c.risk_rating,
    c.current_customer,

    coalesce(s.total_bookings, 0) as total_bookings,
    coalesce(s.total_booked_capacity_mw, 0) as total_booked_capacity_mw,
    coalesce(s.total_gas_volume_mwh, 0) as total_gas_volume_mwh,
    s.avg_ttf_price_eur_mwh,
    s.avg_nbp_price_eur_mwh,

    ct.start_date as contract_start_date,
    ct.end_date as contract_end_date,
    ct.price_eur_per_mwh as contract_price_eur_per_mwh,

    case
        when c.risk_rating = 'High' then 'High Risk'
        when c.credit_status in ('Blocked', 'Suspended') then 'High Risk'
        when c.credit_limit_eur < 50000 then 'Medium Risk'
        else 'Low Risk'
    end as customer_risk_category

from customer c
left join sales s
    on c.customer_id = s.customer_id
left join contract ct
    on c.contract_id = ct.contract_id