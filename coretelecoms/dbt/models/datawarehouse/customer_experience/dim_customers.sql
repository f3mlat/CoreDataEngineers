{{ 
    config(materialized='table'),
    partition_by={'field': 'date_of_birth', 'data_type': 'date'},
    cluster_by=['customer_id']
 }}

select
    customer_id,
    customer_name,
    gender,
    date_of_birth,
    signup_date,
    email,
    address
from {{ ref('stg_customers') }}