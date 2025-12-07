{{ config(materialized='table') }}

with customer_age as (

    select
        customer_id,
        customer_name,
        date_of_birth,
        date_diff(current_date(), date_of_birth, YEAR) as customer_age,
        {{ get_customer_age_group("date_diff(current_date(), date_of_birth, YEAR)") }} as age_group
    from {{ ref('stg_customers') }}

)

select *
from customer_age
