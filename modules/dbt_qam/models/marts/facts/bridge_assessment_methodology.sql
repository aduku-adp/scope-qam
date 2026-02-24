with base as (
    select *
    from {{ ref('stg_rating_methodologies') }}
),
entity_joined as (
    select
        b.*,
        e.entity_key
    from base b
    left join {{ ref('dim_entity') }} e
        on b.entity_name = e.entity_name
),
methodology_joined as (
    select
        e.*,
        m.methodology_key
    from entity_joined e
    left join {{ ref('dim_methodology') }} m
        on e.methodology_name = m.methodology_name
)
select
    md5(record_hash || '|' || methodology_name) as assessment_methodology_key,
    record_hash,
    entity_key,
    to_char(assessment_date, 'YYYYMMDD')::int as assessment_date_key,
    methodology_key,
    methodology_name,
    source_system,
    document_version
from methodology_joined
