with src as (
    select *
    from {{ source('raw', 'rating_assessments_history') }}
),
normalized as (
    select
        id,
        record_hash,
        entity_information as entity_information_json,
        methodology as methodology_json,
        industry_risk as industry_risk_json,
        business_risk_profile as business_risk_profile_json,
        financial_risk_profile as financial_risk_profile_json,
        credit_metrics as credit_metrics_json,
        entity_name,
        country,
        industry,
        business_risk_score,
        financial_risk_score,
        rating_date,
        source_file_path,
        source_modified_at_utc,
        ingested_at
    from src
)
select
    id,
    record_hash,
    coalesce(entity_name, entity_information_json ->> 'name') as entity_name,
    coalesce(country, entity_information_json ->> 'country_of_origin') as country,
    coalesce(industry, entity_information_json ->> 'industry') as industry,
    entity_information_json ->> 'corporate_sector' as corporate_sector,
    entity_information_json ->> 'reporting_currency' as reporting_currency,
    entity_information_json ->> 'accounting_principles' as accounting_principles,
    entity_information_json ->> 'fiscal_year_end' as fiscal_year_end,
    industry_risk_json ->> 'industry_classification' as industry_classification,
    industry_risk_json ->> 'industry_risk_score' as industry_risk_score,
    nullif(industry_risk_json ->> 'industry_weight', '')::numeric as industry_weight,
    industry_risk_json ->> 'segmentation_criteria' as segmentation_criteria,
    coalesce(business_risk_score, business_risk_profile_json ->> 'overall_score') as business_risk_score,
    business_risk_profile_json -> 'components' ->> 'blended_industry_risk_profile' as blended_industry_risk_profile,
    business_risk_profile_json -> 'components' ->> 'competitive_positioning' as competitive_positioning,
    business_risk_profile_json -> 'components' ->> 'market_share' as market_share,
    business_risk_profile_json -> 'components' ->> 'diversification' as diversification,
    business_risk_profile_json -> 'components' ->> 'operating_profitability' as operating_profitability,
    business_risk_profile_json -> 'components' ->> 'sector_company_specific_factors_1' as sector_company_specific_factors_1,
    business_risk_profile_json -> 'components' ->> 'sector_company_specific_factors_2' as sector_company_specific_factors_2,
    coalesce(financial_risk_score, financial_risk_profile_json ->> 'overall_score') as financial_risk_score,
    financial_risk_profile_json -> 'components' ->> 'leverage' as leverage,
    financial_risk_profile_json -> 'components' ->> 'interest_cover' as interest_cover,
    financial_risk_profile_json -> 'components' ->> 'cash_flow_cover' as cash_flow_cover,
    nullif(financial_risk_profile_json -> 'components' ->> 'liquidity_adjustment_notches', '')::int as liquidity_adjustment_notches,
    rating_date,
    source_file_path,
    source_modified_at_utc,
    ingested_at,
    methodology_json,
    credit_metrics_json
from normalized
