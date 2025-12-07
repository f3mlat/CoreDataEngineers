{{ config(materialized='view') }}

select
  id as agent_id,
  trim(name) as agent_name,
  trim(experience) as agent_rank,
  trim(state) as state,
  ingestion_date,
  ingestion_timestamp
from {{ source('staging', 'agents') }}