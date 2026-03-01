{{
  config(
    materialized='incremental',
    unique_key='assessment_industry_risk_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

with base as (
    select *
    from {{ ref('stg_industry_risks') }}
),
industry_risk_joined as (
    select
        b.*,
        d.industry_risk_key
    from base b
    left join {{ ref('dim_industry_risk') }} d
        on coalesce(b.industry_classification, '') = coalesce(d.industry_classification, '')
       and coalesce(b.industry_risk_score, '') = coalesce(d.industry_risk_score, '')
)
select
    md5(
        record_hash || '|' ||
        coalesce(industry_classification, '') || '|' ||
        coalesce(industry_risk_score, '') || '|' ||
        coalesce(industry_risk_index::text, '') || '|' ||
        document_version::text
    ) as assessment_industry_risk_key,
    record_hash,
    company_id,
    document_version,
    to_char(source_modified_date, 'YYYYMMDD')::int as source_modified_date_key,
    industry_risk_key,
    industry_risk_index,
    industry_classification,
    industry_risk_score,
    industry_weight,
    source_file_path,
    source_modified_at_utc
from industry_risk_joined
