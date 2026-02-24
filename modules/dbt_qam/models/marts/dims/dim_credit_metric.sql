with base as (
    select distinct metric_name
    from {{ ref('stg_credit_metrics') }}
)
select
    md5(metric_name) as metric_key,
    metric_name
from base
