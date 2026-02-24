with base as (
    select
        record_hash,
        entity_name,
        assessment_date,
        source_system,
        document_version,
        credit_metrics_json
    from {{ ref('stg_rating_assessments_history') }}
),
metrics as (
    select
        b.record_hash,
        b.entity_name,
        b.assessment_date,
        b.source_system,
        b.document_version,
        metric_obj
    from base b
    cross join lateral jsonb_array_elements(coalesce(b.credit_metrics_json, '[]'::jsonb)) as metric_obj
),
metric_values as (
    select
        m.record_hash,
        m.entity_name,
        m.assessment_date,
        m.source_system,
        m.document_version,
        m.metric_obj ->> 'metric' as metric_name,
        coalesce((m.metric_obj ->> 'locked')::boolean, false) as locked,
        value_obj
    from metrics m
    cross join lateral jsonb_array_elements(coalesce(m.metric_obj -> 'values', '[]'::jsonb)) as value_obj
)
select
    record_hash,
    entity_name,
    assessment_date,
    source_system,
    document_version,
    metric_name,
    value_obj ->> 'year' as year_label,
    (right(value_obj ->> 'year', 1) = 'E') as is_estimate,
    nullif(value_obj ->> 'value', '')::numeric as metric_value,
    locked
from metric_values
