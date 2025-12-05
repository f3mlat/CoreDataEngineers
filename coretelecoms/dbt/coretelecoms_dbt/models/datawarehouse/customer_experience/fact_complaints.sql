{{ config(materialized='table') }}

with all_complaints as (
    select
        *
    from {{ ref('int_all_complaints') }}
),
final as (
    select
        c.complaint_id,
        c.customer_id,
        cust.customer_name,
        cust.location,
        c.agent_id,
        a.agent_name,
        c.source_system,
        c.issue_type,
        c.resolution_status,
        c.complaint_date,
        c.ingestion_date
    from all_complaints c
    left join {{ ref('dim_customers') }} cust on c.customer_id = cust.customer_id
    left join {{ ref('dim_agents') }} a on c.agent_id = a.agent_id
)

select
    *
from final