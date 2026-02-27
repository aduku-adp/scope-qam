{{
  config(
    materialized='incremental',
    incremental_strategy='append'
  )
}}

with assessment as (
    select
        ranked.assessment_key,
        ranked.record_hash,
        ranked.company_id,
        ranked.document_version,
        ranked.source_modified_date_key,
        ranked.source_modified_date,
        ranked.source_file_path,
        ranked.source_modified_at_utc,
        ranked.ingested_at,
        ranked.industry_risk_score as assessment_industry_risk_score,
        ranked.industry_weight as assessment_industry_weight,
        ranked.segmentation_criteria as assessment_segmentation_criteria,
        ranked.business_risk_score,
        ranked.financial_risk_score,
        ranked.blended_industry_risk_profile,
        ranked.competitive_positioning,
        ranked.market_share,
        ranked.diversification,
        ranked.operating_profitability,
        ranked.sector_company_specific_factors_1,
        ranked.sector_company_specific_factors_2,
        ranked.leverage,
        ranked.interest_cover,
        ranked.cash_flow_cover,
        ranked.liquidity_adjustment_notches
    from (
        select
            fa.*,
            row_number() over (
                partition by fa.company_id
                order by
                    fa.document_version desc,
                    fa.source_modified_at_utc desc,
                    fa.ingested_at desc,
                    fa.assessment_key desc
            ) as rn
        from {{ ref('fct_rating_assessment') }} fa
    ) ranked
    where ranked.rn = 1
),
company_as_of as (
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
        dc.industry_weight as dim_industry_weight,
        dc.segmentation_criteria as dim_segmentation_criteria,
        dc.rating_methodologies_applied,
        dc.start_at,
        dc.end_at,
        dc.is_active,
        row_number() over (
            partition by a.assessment_key
            order by dc.start_at desc, dc.document_version desc
        ) as rn
    from assessment a
    left join {{ ref('dim_company') }} dc
        on dc.company_id = a.company_id
       and dc.is_active = true
       and dc.start_at <= coalesce(a.source_modified_at_utc, a.ingested_at)
       and (dc.end_at is null or dc.end_at > coalesce(a.source_modified_at_utc, a.ingested_at))
),
company_one as (
    select *
    from company_as_of
    where rn = 1
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
    md5(a.assessment_key || '|' || '{{ invocation_id }}') as snapshot_id,
    '{{ invocation_id }}'::text as snapshot_run_id,
    now()::timestamptz as snapshot_created_at,
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
    coalesce(c.dim_industry_weight, ir.industry_weights, a.assessment_industry_weight) as industry_weight,
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
    m.methodology_items,
    ir.industry_risk_items,
    cm.credit_metrics
from assessment a
left join company_one c
    on a.assessment_key = c.assessment_key
left join methodology_agg m
    on a.assessment_key = m.assessment_key
left join industry_risk_agg ir
    on a.assessment_key = ir.assessment_key
left join credit_metric_agg cm
    on a.assessment_key = cm.assessment_key
