{{ config(materialized='view') }}

select
  trim(request_id) as complaint_id,
  trim(customer_id) as customer_id,
  agent_id,
  lower(trim(complaint_catego_ry)) as complaint_category,
  lower(trim(resolutionstatus)) as resolution_status,
  DATE(SAFE_CAST(request_date AS TIMESTAMP)) as request_date,
  DATE(SAFE_CAST(resolution_date AS TIMESTAMP)) as resolution_date,
  DATE(SAFE_CAST(webformgenerationdate AS TIMESTAMP)) as web_form_generation_date,
  ingestion_date,
  ingestion_timestamp  
from {{ source('staging', 'web_complaints') }}