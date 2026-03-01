{{
  config(
    materialized='incremental',
    unique_key='metric_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

-- Dictionary dimension for credit metric names.
with base as (
    select distinct metric_name
    from {{ ref('stg_credit_metrics') }}
)
select
    md5(metric_name) as metric_key,
    metric_name
from base
