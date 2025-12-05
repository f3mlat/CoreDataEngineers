{{ config(materialized='view') }}

select
  agent_id,
  agent_name,
  department,
  ingestion_timestamp,
  DATE(SAFE_CAST(ingestion_timestamp AS TIMESTAMP)) as ingestion_date
from {{ source('raw', 'agents') }}