{{ config(materialized='view') }}

select
  post_id,
  customer_id,
  agent_id,
  lower(trim(platform)) as platform,
  lower(trim(issue)) as issue,
  lower(trim(sentiment)) as sentiment,
  SAFE_CAST(ingestion_timestamp AS TIMESTAMP) as ingestion_timestamp,
  DATE(SAFE_CAST(ingestion_timestamp AS TIMESTAMP)) as ingestion_date
from {{ source('raw', 'social') }}