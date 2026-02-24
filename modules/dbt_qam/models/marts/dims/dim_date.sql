with dates as (
    select distinct assessment_date as full_date
    from {{ ref('stg_rating_assessments_history') }}
    where assessment_date is not null
)
select
    to_char(full_date, 'YYYYMMDD')::int as date_key,
    full_date,
    extract(year from full_date)::int as year,
    extract(month from full_date)::int as month,
    extract(day from full_date)::int as day,
    to_char(full_date, 'YYYY-MM') as year_month,
    extract(quarter from full_date)::int as quarter
from dates
