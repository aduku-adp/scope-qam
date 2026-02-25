with base as (
    select
        record_hash,
        entity_name,
        rating_date,
        source_file_path,
        source_modified_at_utc,
        methodology_json
    from {{ ref('stg_rating_assessments_history') }}
),
exploded as (
    select
        b.record_hash,
        b.entity_name,
        b.rating_date,
        b.source_file_path,
        b.source_modified_at_utc,
        jsonb_array_elements_text(coalesce(b.methodology_json -> 'rating_methodologies_applied', '[]'::jsonb)) as methodology_name
    from base b
)
select *
from exploded
