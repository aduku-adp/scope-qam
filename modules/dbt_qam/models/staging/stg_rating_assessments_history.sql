with src as (
    select *
    from {{ source('raw', 'rating_assessments_history') }}
),
normalized as (
    select
        id,
        record_hash,
        company_key,
        document_version,
        company_information as company_information_json,
        coalesce(methodology, company_information -> 'methodology') as methodology_json,
        coalesce(industry_risk, company_information -> 'industry_risk') as industry_risk_raw_json,
        business_risk_profile as business_risk_profile_json,
        financial_risk_profile as financial_risk_profile_json,
        credit_metrics as credit_metrics_json,
        company_name,
        country,
        corporate_sector,
        segmentation_criteria,
        business_risk_score,
        financial_risk_score,
        source_file_path,
        source_modified_at_utc,
        ingested_at
    from src
),
parsed as (
    select
        n.*,
        case
            when jsonb_typeof(industry_risk_raw_json) = 'array' then industry_risk_raw_json
            when jsonb_typeof(industry_risk_raw_json) = 'object' then jsonb_build_array(industry_risk_raw_json)
            else '[]'::jsonb
        end as industry_risk_list_json
    from normalized n
)
select
    id,
    record_hash,
    company_key,
    document_version,
    coalesce(company_name, company_information_json ->> 'name') as company_name,
    coalesce(country, company_information_json ->> 'country_of_origin') as country,
    coalesce(corporate_sector, company_information_json ->> 'corporate_sector') as corporate_sector,
    company_information_json ->> 'reporting_currency' as reporting_currency,
    company_information_json ->> 'accounting_principles' as accounting_principles,
    company_information_json ->> 'fiscal_year_end' as fiscal_year_end,
    (
        select string_agg(elem ->> 'industry_classification', ' | ' order by ord)
        from jsonb_array_elements(industry_risk_list_json) with ordinality as e(elem, ord)
    ) as industry_classification,
    (
        select string_agg(elem ->> 'industry_risk_score', ' | ' order by ord)
        from jsonb_array_elements(industry_risk_list_json) with ordinality as e(elem, ord)
    ) as industry_risk_score,
    (
        select sum(nullif(elem ->> 'industry_weight', '')::numeric)
        from jsonb_array_elements(industry_risk_list_json) as e(elem)
    ) as industry_weight,
    coalesce(
        segmentation_criteria,
        company_information_json ->> 'segmentation_criteria',
        case
            when jsonb_typeof(industry_risk_raw_json) = 'object'
                then industry_risk_raw_json ->> 'segmentation_criteria'
            else null
        end
    ) as segmentation_criteria,
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
    source_modified_at_utc::date as source_modified_date,
    source_file_path,
    source_modified_at_utc,
    ingested_at,
    methodology_json,
    industry_risk_list_json,
    credit_metrics_json
from parsed
