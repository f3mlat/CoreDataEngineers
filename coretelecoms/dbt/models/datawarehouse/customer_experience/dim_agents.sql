{{ config(materialized='table') }}

select
    agent_id,
    agent_name,
    agent_rank,
    state
from {{ ref('stg_agents') }}