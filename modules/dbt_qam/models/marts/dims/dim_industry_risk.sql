{{
  config(
    materialized='incremental',
    unique_key='industry_risk_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

-- Dictionary dimension for normalized industry-risk combinations.
with base as (
    select distinct
        industry_classification,
        industry_risk_score
    from {{ ref('stg_industry_risks') }}
)
select
    md5(coalesce(industry_classification, '') || '|' || coalesce(industry_risk_score, '')) as industry_risk_key,
    industry_classification,
    industry_risk_score
from base
