with base as (
    select *
    from {{ ref('stg_credit_metrics') }}
),
entity_joined as (
    select
        b.*,
        e.entity_key
    from base b
    left join {{ ref('dim_entity') }} e
        on b.entity_name = e.entity_name
),
metric_joined as (
    select
        e.*,
        m.metric_key
    from entity_joined e
    left join {{ ref('dim_credit_metric') }} m
        on e.metric_name = m.metric_name
)
select
    md5(record_hash || '|' || metric_name || '|' || year_label) as credit_metric_value_key,
    record_hash,
    entity_key,
    metric_key,
    to_char(rating_date, 'YYYYMMDD')::int as rating_date_key,
    rating_date,
    year_label,
    is_estimate,
    metric_value,
    locked,
    source_file_path,
    source_modified_at_utc
from metric_joined
