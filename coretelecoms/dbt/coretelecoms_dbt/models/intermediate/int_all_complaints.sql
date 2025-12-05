{{ config(materialized='table') }}

select
    call_id as complaint_id,
    customer_id,
    agent_id,
    'call_center' as source_system,
    complaint_type as issue_type,
    resolution_status,
    call_date as complaint_date
from {{ ref('stg_call_center') }}

union all

select
    complaint_id,
    customer_id,
    agent_id,
    'social_media',
    issue_type,
    resolution_status,
    complaint_date
from {{ ref('stg_social_media') }}

union all

select
    form_id as complaint_id,
    customer_id,
    agent_id,
    'web_form',
    complaint_type,
    resolution_status,
    submitted_at::date
from {{ ref('stg_web_complaints') }}