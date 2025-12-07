{{ config(materialized='view') }}

select
  call_id,
  trim(customer_id) as customer_id,
  agent_id,
  lower(trim(complaint_catego_ry)) as complaint_category,
  DATE(SAFE_CAST(call_start_time AS TIMESTAMP)) as call_start_date,
  DATE(SAFE_CAST(call_end_time AS TIMESTAMP)) as call_end_date,
  lower(trim(resolutionstatus)) as resolution_status,
  DATE(SAFE_CAST(calllogsgenerationdate AS TIMESTAMP)) as call_generation_date,
  ingestion_date,
  ingestion_timestamp
from {{ source('staging', 'call_center_logs') }}