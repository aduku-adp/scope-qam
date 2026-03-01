{{
  config(
    materialized='incremental',
    unique_key='rep_company_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

-- Reporting-wide denormalized company table that joins dims/facts at version grain.
-- This is the primary source for company API endpoints.
with assessment as (
    select
        fa.assessment_key,
        fa.record_hash,
        fa.company_id,
        fa.document_version,
        fa.source_modified_date_key,
        fa.source_modified_date,
        fa.source_file_path,
        fa.source_modified_at_utc,
        fa.ingested_at,
        fa.industry_risk_score as assessment_industry_risk_score,
        fa.industry_weight as assessment_industry_weight,
        fa.segmentation_criteria as assessment_segmentation_criteria,
        fa.business_risk_score,
        fa.financial_risk_score,
        fa.blended_industry_risk_profile,
        fa.competitive_positioning,
        fa.market_share,
        fa.diversification,
        fa.operating_profitability,
        fa.sector_company_specific_factors_1,
        fa.sector_company_specific_factors_2,
        fa.leverage,
        fa.interest_cover,
        fa.cash_flow_cover,
        fa.liquidity_adjustment_notches
    from {{ ref('fct_rating_assessment') }} fa
),
company_version as (
    select
        a.assessment_key,
        dc.company_scd_key,
        dc.company_name,
        dc.country,
        dc.corporate_sector,
        dc.reporting_currency,
        dc.accounting_principles,
        dc.fiscal_year_end,
        dc.industry_classification,
        dc.industry_risk_score as dim_industry_risk_score,
        dc.industry_weight as dim_industry_risk_weight,
        dc.segmentation_criteria as dim_segmentation_criteria,
        dc.rating_methodologies_applied,
        dc.start_at,
        dc.end_at,
        dc.is_active
    from assessment a
    left join {{ ref('dim_company') }} dc
        on dc.company_id = a.company_id
       and dc.document_version = a.document_version
),
methodology_agg as (
    select
        a.assessment_key,
        string_agg(dm.methodology_name, ' | ' order by dm.methodology_name) as methodology_names,
        jsonb_agg(
            jsonb_build_object(
                'methodology_key', dm.methodology_key,
                'methodology_name', dm.methodology_name
            )
            order by dm.methodology_name
        ) as methodology_items
    from assessment a
    left join {{ ref('bridge_assessment_methodology') }} bam
        on a.record_hash = bam.record_hash
       and a.company_id = bam.company_id
       and a.document_version = bam.document_version
    left join {{ ref('dim_methodology') }} dm
        on bam.methodology_key = dm.methodology_key
    group by a.assessment_key
),
industry_risk_agg as (
    select
        a.assessment_key,
        string_agg(dir.industry_classification, ' | ' order by bai.industry_risk_index) as industry_classifications,
        string_agg(dir.industry_risk_score, ' | ' order by bai.industry_risk_index) as industry_risk_scores,
        string_agg(bai.industry_weight::text, ' | ' order by bai.industry_risk_index) as industry_weights,
        jsonb_agg(
            jsonb_build_object(
                'industry_risk_key', dir.industry_risk_key,
                'industry_classification', dir.industry_classification,
                'industry_risk_score', dir.industry_risk_score,
                'industry_weight', bai.industry_weight,
                'industry_risk_index', bai.industry_risk_index
            )
            order by bai.industry_risk_index
        ) as industry_risk_items
    from assessment a
    left join {{ ref('bridge_assessment_industry_risk') }} bai
        on a.record_hash = bai.record_hash
       and a.company_id = bai.company_id
       and a.document_version = bai.document_version
    left join {{ ref('dim_industry_risk') }} dir
        on bai.industry_risk_key = dir.industry_risk_key
    group by a.assessment_key
),
credit_metric_points as (
    select
        a.assessment_key,
        dcm.metric_name,
        cmv.year_label,
        cmv.is_estimate,
        cmv.metric_value,
        cmv.locked
    from assessment a
    left join {{ ref('fct_credit_metric_value') }} cmv
        on a.record_hash = cmv.record_hash
       and a.document_version = cmv.document_version
       and a.company_id = cmv.company_id
    left join {{ ref('dim_credit_metric') }} dcm
        on cmv.metric_key = dcm.metric_key
    where cmv.credit_metric_value_key is not null
),
credit_metric_agg as (
    select
        assessment_key,
        jsonb_agg(
            jsonb_build_object(
                'metric_name', metric_name,
                'year_label', year_label,
                'is_estimate', is_estimate,
                'metric_value', metric_value,
                'locked', locked
            )
            order by metric_name, year_label
        ) as credit_metrics
    from credit_metric_points
    group by assessment_key
)
select
    a.assessment_key as rep_company_key,
    a.assessment_key,
    a.record_hash,
    a.company_id,
    c.company_scd_key,
    coalesce(c.company_name, a.company_id) as company_name,
    c.country,
    c.corporate_sector,
    c.reporting_currency,
    c.accounting_principles,
    c.fiscal_year_end,
    coalesce(c.industry_classification, ir.industry_classifications) as industry_classification,
    coalesce(c.dim_industry_risk_score, ir.industry_risk_scores, a.assessment_industry_risk_score) as industry_risk_score,
    coalesce(c.dim_industry_risk_weight, ir.industry_weights, a.assessment_industry_weight) as industry_weight,
    coalesce(c.dim_segmentation_criteria, a.assessment_segmentation_criteria) as segmentation_criteria,
    coalesce(c.rating_methodologies_applied, m.methodology_names) as rating_methodologies_applied,
    a.document_version,
    c.start_at,
    c.end_at,
    c.is_active,
    a.source_modified_date_key,
    a.source_modified_date,
    a.source_file_path,
    a.source_modified_at_utc,
    a.ingested_at,
    a.business_risk_score,
    a.financial_risk_score,
    a.blended_industry_risk_profile,
    a.competitive_positioning,
    a.market_share,
    a.diversification,
    a.operating_profitability,
    a.sector_company_specific_factors_1,
    a.sector_company_specific_factors_2,
    a.leverage,
    a.interest_cover,
    a.cash_flow_cover,
    a.liquidity_adjustment_notches,
    cm.credit_metrics
from assessment a
left join company_version c
    on a.assessment_key = c.assessment_key
left join methodology_agg m
    on a.assessment_key = m.assessment_key
left join industry_risk_agg ir
    on a.assessment_key = ir.assessment_key
left join credit_metric_agg cm
    on a.assessment_key = cm.assessment_key
