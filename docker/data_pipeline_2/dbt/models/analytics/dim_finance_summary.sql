-- Analytics model
-- Simple summary: average Value per year

with cleaned as (
    select
        year,
        CASE
            WHEN value ~ '^[0-9]+$' THEN CAST(value as NUMERIC)
            ELSE 0
        END AS value
    from {{ ref('stg_finance') }}
)

select
    year,
    AVG(value) as avg_value
from cleaned
group by year
order by year