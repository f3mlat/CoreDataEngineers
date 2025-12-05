-- Ensure no duplicate complaints
select
    complaint_id
from {{ ref('fact_complaints') }}
group by complaint_id
having count(*) > 1