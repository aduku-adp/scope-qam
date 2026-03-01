{{
  config(
    materialized='incremental',
    unique_key='assessment_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

-- Core assessment fact table at one row per raw assessment record hash.
with base as (
    select *
    from {{ ref('stg_rating_assessments_history') }}
)
select
    md5(record_hash) as assessment_key,
    record_hash,
    company_id,
    document_version,
    to_char(source_modified_date, 'YYYYMMDD')::int as source_modified_date_key,
    source_modified_date,
    source_file_path,
    source_modified_at_utc,
    industry_risk_score,
    industry_weight,
    segmentation_criteria,
    business_risk_score,
    financial_risk_score,
    blended_industry_risk_profile,
    competitive_positioning,
    market_share,
    diversification,
    operating_profitability,
    sector_company_specific_factors_1,
    sector_company_specific_factors_2,
    leverage,
    interest_cover,
    cash_flow_cover,
    liquidity_adjustment_notches,
    ingested_at
from base
