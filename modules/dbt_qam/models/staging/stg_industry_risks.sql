-- Explode industry-risk JSON array so each industry component is queryable.
with base as (
    select
        record_hash,
        company_id,
        document_version,
        company_name,
        source_modified_date,
        source_file_path,
        source_modified_at_utc,
        industry_risk_list_json
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
        elem,
        ord::int as industry_risk_index
    from base b
    cross join lateral jsonb_array_elements(coalesce(b.industry_risk_list_json, '[]'::jsonb)) with ordinality as e(elem, ord)
)
select
    record_hash,
    company_id,
    document_version,
    company_name,
    source_modified_date,
    source_file_path,
    source_modified_at_utc,
    industry_risk_index,
    elem ->> 'industry_classification' as industry_classification,
    elem ->> 'industry_risk_score' as industry_risk_score,
    nullif(elem ->> 'industry_weight', '')::numeric as industry_weight
from exploded
