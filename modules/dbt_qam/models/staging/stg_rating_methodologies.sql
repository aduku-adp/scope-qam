with base as (
    select
        record_hash,
        company_id,
        document_version,
        company_name,
        source_modified_date,
        source_file_path,
        source_modified_at_utc,
        methodology_json
    from {{ ref('stg_rating_assessments_history') }}
),
exploded as (
    select
        b.record_hash,
        b.company_id,
        b.document_version,
        b.company_name,
        b.source_modified_date,
        b.source_file_path,
        b.source_modified_at_utc,
        jsonb_array_elements_text(coalesce(b.methodology_json -> 'rating_methodologies_applied', '[]'::jsonb)) as methodology_name
    from base b
)
select *
from exploded
