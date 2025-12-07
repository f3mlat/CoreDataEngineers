{{ config(materialized='view') }}

select
    trim(customer_id) as customer_id,
    trim(name) as customer_name,
    trim(gender) as gender,
    DATE(SAFE_CAST(date_of_birth AS TIMESTAMP)) as date_of_birth,
    DATE(SAFE_CAST(signup_date AS TIMESTAMP)) as signup_date,
    case
        when email is null or email = '' then null
        when REGEXP_CONTAINS(email, r'^[^@]+@[^@]+\.[^@]+$') then email
        else null
    end as email,
    trim(address) as address,    
    ingestion_date,
    ingestion_timestamp
from {{ source('staging', 'customers') }}
where customer_id is not null