with base as (
    select *
    from {{ ref('stg_rating_assessments_history') }}
),
entity_joined as (
    select
        b.*,
        e.entity_key
    from base b
    left join {{ ref('dim_entity') }} e
        on b.entity_name = e.entity_name
       and coalesce(b.country, '') = coalesce(e.country, '')
       and coalesce(b.industry, '') = coalesce(e.industry, '')
)
select
    md5(record_hash) as assessment_key,
    record_hash,
    entity_key,
    to_char(assessment_date, 'YYYYMMDD')::int as assessment_date_key,
    assessment_date,
    source_system,
    document_version,
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
from entity_joined
