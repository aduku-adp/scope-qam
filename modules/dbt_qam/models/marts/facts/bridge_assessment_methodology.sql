with base as (
    select *
    from {{ ref('stg_rating_methodologies') }}
),
methodology_joined as (
    select
        b.*,
        m.methodology_key
    from base b
    left join {{ ref('dim_methodology') }} m
        on b.methodology_name = m.methodology_name
)
select
    md5(record_hash || '|' || methodology_name || '|' || document_version::text) as assessment_methodology_key,
    record_hash,
    company_key,
    document_version,
    to_char(source_modified_date, 'YYYYMMDD')::int as source_modified_date_key,
    methodology_key,
    methodology_name,
    source_file_path,
    source_modified_at_utc
from methodology_joined
