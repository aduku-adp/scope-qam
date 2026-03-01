-- Explode nested credit_metrics JSON array into one row per metric point.
with base as (
    select
        record_hash,
        company_id,
        document_version,
        company_name,
        source_modified_date,
        source_file_path,
        source_modified_at_utc,
        credit_metrics_json
    from {{ ref('stg_rating_assessments_history') }}
),
metrics as (
    select
        b.record_hash,
        b.company_id,
        b.document_version,
        b.company_name,
        b.source_modified_date,
        b.source_file_path,
        b.source_modified_at_utc,
        metric_obj
    from base b
    cross join lateral jsonb_array_elements(coalesce(b.credit_metrics_json, '[]'::jsonb)) as metric_obj
),
metric_values as (
    select
        m.record_hash,
        m.company_id,
        m.document_version,
        m.company_name,
        m.source_modified_date,
        m.source_file_path,
        m.source_modified_at_utc,
        m.metric_obj ->> 'metric' as metric_name,
        coalesce((m.metric_obj ->> 'locked')::boolean, false) as locked,
        value_obj
    from metrics m
    cross join lateral jsonb_array_elements(coalesce(m.metric_obj -> 'values', '[]'::jsonb)) as value_obj
)
select
    record_hash,
    company_id,
    document_version,
    company_name,
    source_modified_date,
    source_file_path,
    source_modified_at_utc,
    metric_name,
    value_obj ->> 'year' as year_label,
    (right(value_obj ->> 'year', 1) = 'E') as is_estimate,
    nullif(value_obj ->> 'value', '')::numeric as metric_value,
    locked
from metric_values
