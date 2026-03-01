{% snapshot snap_company %}

{{
    config(
      target_schema='snapshots',
      unique_key='rep_company_key',
      strategy='timestamp',
      updated_at='source_modified_at_utc',
      invalidate_hard_deletes=True
    )
}}

select
    current_timestamp as snapshot_created_at,
    rep_company_key,
    company_id,
    company_scd_key,
    company_name,
    country,
    corporate_sector,
    reporting_currency,
    accounting_principles,
    fiscal_year_end,
    industry_classification,
    industry_risk_score,
    industry_weight,
    segmentation_criteria,
    rating_methodologies_applied,
    document_version,
    source_file_path,
    source_modified_at_utc,
    business_risk_score,
    financial_risk_score,
    blended_industry_risk_profile,
    competitive_positioning,
    market_share,
    diversification,
    operating_profitability,
    sector_company_specific_factors_1,
    sector_company_specific_factors_2,
    leverage,
    interest_cover,
    cash_flow_cover,
    liquidity_adjustment_notches,
    credit_metrics
from {{ ref('rep_company') }}
where is_active = true

{% endsnapshot %}
