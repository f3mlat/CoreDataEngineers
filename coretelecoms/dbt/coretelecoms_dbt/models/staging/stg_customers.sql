{{ config(materialized='view') }}

select
    customer_id,
    trim(upper(name)) as customer_name,
    gender,
    phone,
    location,
    lower(email) as email_clean,
    ingestion_date
from {{ source('raw', 'raw_customers') }}
where customer_id is not null