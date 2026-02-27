with rating_base as (
    select
        company_id,
        document_version,
        source_modified_date_key,
        source_modified_date,
        source_file_path,
        source_modified_at_utc,
        record_hash,
        industry_risk_score,
        industry_weight,
        segmentation_criteria,
        business_risk_score,
        financial_risk_score
    from {{ ref('fct_rating_assessment') }}
),
rating_points as (
    select
        rb.company_id,
        rb.document_version,
        rb.source_modified_date_key,
        rb.source_modified_date,
        rb.source_file_path,
        rb.source_modified_at_utc as event_time,
        rb.source_modified_at_utc,
        'rating' as series_type,
        p.series_name,
        p.series_value,
        null::text as year_label,
        null::boolean as is_estimate
    from rating_base rb
    cross join lateral (
        values
            ('industry_risk_score', rb.industry_risk_score),
            ('industry_weight', rb.industry_weight),
            ('segmentation_criteria', rb.segmentation_criteria),
            ('business_risk_score', rb.business_risk_score),
            ('financial_risk_score', rb.financial_risk_score)
    ) as p(series_name, series_value)
    where p.series_value is not null
),
credit_base as (
    select
        cmv.company_id,
        cmv.document_version,
        cmv.source_modified_date_key,
        cmv.source_modified_date,
        cmv.source_file_path,
        cmv.source_modified_at_utc,
        cmv.year_label,
        cmv.is_estimate,
        cm.metric_name,
        cmv.metric_value
    from {{ ref('fct_credit_metric_value') }} cmv
    left join {{ ref('dim_credit_metric') }} cm
        on cmv.metric_key = cm.metric_key
),
credit_points as (
    select
        cb.company_id,
        cb.document_version,
        cb.source_modified_date_key,
        cb.source_modified_date,
        cb.source_file_path,
        cb.source_modified_at_utc as event_time,
        cb.source_modified_at_utc,
        'credit_metric' as series_type,
        coalesce(cb.metric_name, 'unknown_metric') as series_name,
        cb.metric_value::text as series_value,
        cb.year_label,
        cb.is_estimate
    from credit_base cb
    where cb.metric_value is not null
),
all_points as (
    select * from rating_points
    union all
    select * from credit_points
),
date_enriched as (
    select
        p.*,
        d.full_date as dim_full_date,
        d.year as dim_year,
        d.month as dim_month,
        d.day as dim_day,
        d.year_month as dim_year_month,
        d.quarter as dim_quarter
    from all_points p
    left join {{ ref('dim_date') }} d
        on p.source_modified_date_key = d.date_key
)
select
    md5(
        company_id || '|' ||
        coalesce(series_type, '') || '|' ||
        coalesce(series_name, '') || '|' ||
        coalesce(year_label, '') || '|' ||
        coalesce(series_value, '') || '|' ||
        document_version::text || '|' ||
        coalesce(event_time::text, '')
    ) as timeseries_key,
    company_id,
    document_version,
    source_modified_date_key,
    source_modified_date,
    dim_full_date,
    dim_year,
    dim_month,
    dim_day,
    dim_year_month,
    dim_quarter,
    source_file_path,
    source_modified_at_utc,
    event_time,
    series_type,
    series_name,
    series_value,
    year_label,
    is_estimate
from date_enriched
