with base as (
    select distinct
        entity_name,
        country,
        industry,
        corporate_sector,
        reporting_currency,
        accounting_principles,
        fiscal_year_end
    from {{ ref('stg_rating_assessments_history') }}
)
select
    md5(coalesce(entity_name, '') || '|' || coalesce(country, '') || '|' || coalesce(industry, '')) as entity_key,
    entity_name,
    country,
    industry,
    corporate_sector,
    reporting_currency,
    accounting_principles,
    fiscal_year_end
from base
