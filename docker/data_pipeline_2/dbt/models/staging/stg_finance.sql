-- Staging model
-- Takes data from the raw "staging_finance" table loaded by ETL
-- Cleans column names and prepares for analytics layer

with source as (
    select *
    from {{ source('staging', 'staging_finance') }}
)

select
    CAST("Year" as INTEGER) as year,
    "Value" as value,
    "Units" as units,
    "Variable_code" as variable_code
from source