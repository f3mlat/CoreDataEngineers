{{ config(materialized='view') }}

select
  call_id,
  customer_id,
  agent_id,
  lower(trim(complaint_type)) as complaint_type,
  SAFE_CAST(duration AS INT64) as duration,
  lower(trim(resolution_status)) as resolution_status,
  SAFE_CAST(ingestion_timestamp AS TIMESTAMP) as ingestion_timestamp,
  DATE(SAFE_CAST(ingestion_timestamp AS TIMESTAMP)) as ingestion_date
from {{ source('raw', 'callcenter') }}