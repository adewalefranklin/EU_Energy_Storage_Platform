{% snapshot snap_customer_master %}

{{
    config(
        target_database='EU_ENERGY_DB',
        target_schema='SNAPSHOTS',
        unique_key='customer_id',
        strategy='check',
        check_cols=[
            'customer_name',
            'contract_id',
            'facility_id',
            'credit_status',
            'credit_limit_eur',
            'risk_rating',
            'current_customer'
        ]
    )
}}

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

{% endsnapshot %}