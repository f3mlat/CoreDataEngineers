{{ config(materialized='table') }}

select
    customer_id,
    customer_name,
    gender,
    date_of_birth,
    signup_date,
    email,
    address
from {{ ref('stg_customers') }}