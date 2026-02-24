with base as (
    select
        record_hash,
        entity_name,
        assessment_date,
        source_system,
        document_version,
        methodology_json
    from {{ ref('stg_rating_assessments_history') }}
),
exploded as (
    select
        b.record_hash,
        b.entity_name,
        b.assessment_date,
        b.source_system,
        b.document_version,
        jsonb_array_elements_text(coalesce(b.methodology_json -> 'rating_methodologies_applied', '[]'::jsonb)) as methodology_name
    from base b
)
select *
from exploded
