{{
  config(
    materialized='incremental',
    unique_key='timeseries_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

-- Unified time-series fact built from rep_company:
-- level 1 = scalar company columns, level 2/3 = exploded credit metric attributes.
with base as (
    select
        company_id,
        document_version,
        source_modified_at_utc as event_time,
        source_modified_at_utc,
        credit_metrics,
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
        liquidity_adjustment_notches
    from {{ ref('rep_company') }}
),
level_1_points as (
    select
        b.company_id,
        b.document_version,
        b.event_time,
        b.source_modified_at_utc,
        v.column_name,
        'value'::text as metric_name,
        v.series_value,
        null::text as year_label,
        null::boolean as is_estimate,
        null::bigint as metric_index
    from base b
    cross join lateral (
        values
            ('company_name', b.company_name::text),
            ('country', b.country::text),
            ('corporate_sector', b.corporate_sector::text),
            ('reporting_currency', b.reporting_currency::text),
            ('accounting_principles', b.accounting_principles::text),
            ('fiscal_year_end', b.fiscal_year_end::text),
            ('industry_classification', b.industry_classification::text),
            ('industry_risk_score', b.industry_risk_score::text),
            ('industry_weight', b.industry_weight::text),
            ('segmentation_criteria', b.segmentation_criteria::text),
            ('rating_methodologies_applied', b.rating_methodologies_applied::text),
            ('business_risk_score', b.business_risk_score::text),
            ('financial_risk_score', b.financial_risk_score::text),
            ('blended_industry_risk_profile', b.blended_industry_risk_profile::text),
            ('competitive_positioning', b.competitive_positioning::text),
            ('market_share', b.market_share::text),
            ('diversification', b.diversification::text),
            ('operating_profitability', b.operating_profitability::text),
            ('sector_company_specific_factors_1', b.sector_company_specific_factors_1::text),
            ('sector_company_specific_factors_2', b.sector_company_specific_factors_2::text),
            ('leverage', b.leverage::text),
            ('interest_cover', b.interest_cover::text),
            ('cash_flow_cover', b.cash_flow_cover::text),
            ('liquidity_adjustment_notches', b.liquidity_adjustment_notches::text)
    ) as v(column_name, series_value)
    where v.series_value is not null
),
credit_metrics_expanded as (
    select
        b.company_id,
        b.document_version,
        b.event_time,
        b.source_modified_at_utc,
        cm.item,
        cm.ordinality as metric_index
    from base b
    cross join lateral jsonb_array_elements(coalesce(b.credit_metrics, '[]'::jsonb)) with ordinality as cm(item, ordinality)
),
level_2_points as (
    select
        e.company_id,
        e.document_version,
        e.event_time,
        e.source_modified_at_utc,
        'credit_metrics'::text as column_name,
        kv.metric_name,
        kv.series_value,
        null::text as year_label,
        case
            when e.item ? 'is_estimate' and e.item->>'is_estimate' in ('true', 'false')
                then (e.item->>'is_estimate')::boolean
            else null::boolean
        end as is_estimate,
        e.metric_index
    from credit_metrics_expanded e
    cross join lateral (
        values
            ('metric_name', e.item->>'metric_name'),
            ('year_label', e.item->>'year_label'),
            ('metric_value', e.item->>'metric_value'),
            ('is_estimate', e.item->>'is_estimate'),
            ('locked', e.item->>'locked')
    ) as kv(metric_name, series_value)
    where kv.series_value is not null
),
level_3_points as (
    select
        e.company_id,
        e.document_version,
        e.event_time,
        e.source_modified_at_utc,
        'credit_metrics'::text as column_name,
        e.item->>'metric_name' as metric_name,
        e.item->>'metric_value' as series_value,
        e.item->>'year_label' as year_label,
        case
            when e.item ? 'is_estimate' and e.item->>'is_estimate' in ('true', 'false')
                then (e.item->>'is_estimate')::boolean
            else null::boolean
        end as is_estimate,
        e.metric_index
    from credit_metrics_expanded e
    where e.item->>'metric_name' is not null
      and e.item->>'metric_value' is not null
),
unioned as (
    select * from level_1_points
    union all
    select * from level_2_points
    union all
    select * from level_3_points
)
select
    md5(
        coalesce(company_id, '')
        || '|'
        || coalesce(document_version::text, '')
        || '|'
        || coalesce(event_time::text, '')
        || '|'
        || coalesce(column_name, '')
        || '|'
        || coalesce(metric_name, '')
        || '|'
        || coalesce(year_label, '')
        || '|'
        || coalesce(series_value, '')
        || '|'
        || coalesce(metric_index::text, '')
    ) as timeseries_key,
    company_id,
    document_version,
    event_time,
    column_name,
    metric_name,
    series_value,
    year_label,
    is_estimate
from unioned
