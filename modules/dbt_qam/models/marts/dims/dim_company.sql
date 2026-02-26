with base as (
    select
        company_key,
        company_name,
        country,
        corporate_sector,
        reporting_currency,
        accounting_principles,
        fiscal_year_end,
        industry_classification,
        industry_risk_score,
        industry_weight,
        segmentation_criteria,
        (
            select string_agg(v, ' | ' order by v)
            from jsonb_array_elements_text(
                coalesce(methodology_json -> 'rating_methodologies_applied', '[]'::jsonb)
            ) as v
        ) as rating_methodologies_applied,
        coalesce(source_modified_at_utc, ingested_at) as effective_ts,
        document_version,
        record_hash
    from {{ ref('stg_rating_assessments_history') }}
),
ordered as (
    select
        *,
        md5(
            coalesce(company_name, '') || '|' ||
            coalesce(country, '') || '|' ||
            coalesce(corporate_sector, '') || '|' ||
            coalesce(reporting_currency, '') || '|' ||
            coalesce(accounting_principles, '') || '|' ||
            coalesce(fiscal_year_end, '') || '|' ||
            coalesce(industry_classification, '') || '|' ||
            coalesce(industry_risk_score, '') || '|' ||
            coalesce(industry_weight::text, '') || '|' ||
            coalesce(segmentation_criteria, '') || '|' ||
            coalesce(rating_methodologies_applied, '')
        ) as attribute_hash,
        lag(
            md5(
                coalesce(company_name, '') || '|' ||
                coalesce(country, '') || '|' ||
                coalesce(corporate_sector, '') || '|' ||
                coalesce(reporting_currency, '') || '|' ||
                coalesce(accounting_principles, '') || '|' ||
                coalesce(fiscal_year_end, '') || '|' ||
                coalesce(industry_classification, '') || '|' ||
                coalesce(industry_risk_score, '') || '|' ||
                coalesce(industry_weight::text, '') || '|' ||
                coalesce(segmentation_criteria, '') || '|' ||
                coalesce(rating_methodologies_applied, '')
            )
        ) over (
            partition by company_key
            order by effective_ts, document_version, record_hash
        ) as prev_attribute_hash
    from base
),
change_points as (
    select
        company_key,
        company_name,
        country,
        corporate_sector,
        reporting_currency,
        accounting_principles,
        fiscal_year_end,
        industry_classification,
        industry_risk_score,
        industry_weight,
        segmentation_criteria,
        rating_methodologies_applied,
        effective_ts as start_at,
        document_version
    from ordered
    where prev_attribute_hash is null or prev_attribute_hash <> attribute_hash
),
scd_rows as (
    select
        company_key,
        company_name,
        country,
        corporate_sector,
        reporting_currency,
        accounting_principles,
        fiscal_year_end,
        industry_classification,
        industry_risk_score,
        industry_weight,
        segmentation_criteria,
        rating_methodologies_applied,
        document_version,
        start_at,
        lead(start_at) over (
            partition by company_key
            order by start_at, document_version
        ) as end_at
    from change_points
)
select
    md5(company_key || '|' || start_at::text) as company_scd_key,
    company_key,
    company_name,
    country,
    corporate_sector,
    reporting_currency,
    accounting_principles,
    fiscal_year_end,
    industry_classification,
    industry_risk_score,
    industry_weight,
    segmentation_criteria,
    rating_methodologies_applied,
    document_version,
    start_at,
    end_at,
    (end_at is null) as is_active
from scd_rows
