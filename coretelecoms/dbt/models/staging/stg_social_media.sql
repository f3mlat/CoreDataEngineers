{{ config(materialized='view') }}

select
  trim(complaint_id) as complaint_id,
  trim(customer_id) as customer_id,
  agent_id,
  lower(trim(complaint_catego_ry)) as complaint_category,
  lower(trim(resolutionstatus)) as resolution_status,
  DATE(SAFE_CAST(request_date AS TIMESTAMP)) as complaint_date,
  DATE(SAFE_CAST(resolution_date AS TIMESTAMP)) as resolution_date,
  lower(trim(media_channel)) as media_channel,
  DATE(SAFE_CAST(mediacomplaintgenerationdate AS TIMESTAMP)) as media_complaint_generation_date,
  ingestion_date,
  ingestion_timestamp  
from {{ source('staging', 'social_media') }}