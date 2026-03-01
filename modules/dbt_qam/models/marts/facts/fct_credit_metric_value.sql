{{
  config(
    materialized='incremental',
    unique_key='credit_metric_value_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

with base as (
    select *
    from {{ ref('stg_credit_metrics') }}
),
metric_joined as (
    select
        b.*,
        m.metric_key
    from base b
    left join {{ ref('dim_credit_metric') }} m
        on b.metric_name = m.metric_name
)
select
    md5(record_hash || '|' || metric_name || '|' || year_label || '|' || document_version::text) as credit_metric_value_key,
    record_hash,
    company_id,
    document_version,
    metric_key,
    to_char(source_modified_date, 'YYYYMMDD')::int as source_modified_date_key,
    source_modified_date,
    year_label,
    is_estimate,
    metric_value,
    locked,
    source_file_path,
    source_modified_at_utc
from metric_joined
