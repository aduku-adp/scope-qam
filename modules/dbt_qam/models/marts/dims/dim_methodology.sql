with base as (
    select distinct methodology_name
    from {{ ref('stg_rating_methodologies') }}
)
select
    md5(methodology_name) as methodology_key,
    methodology_name
from base
