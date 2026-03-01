{% macro _create_index_if_table_exists(schema_name, table_name, index_name, columns_sql, where_sql=None) %}
  {%- set relation = adapter.get_relation(
      database=target.database,
      schema=schema_name,
      identifier=table_name
  ) -%}

  {%- if relation is not none -%}
    {%- set ddl -%}
      create index if not exists {{ index_name }}
      on {{ schema_name }}.{{ table_name }} ({{ columns_sql }})
      {%- if where_sql %} where {{ where_sql }}{% endif -%}
    {%- endset -%}
    {% do run_query(ddl) %}
  {%- endif -%}
{% endmacro %}

{% macro ensure_performance_indexes() %}
  {# dims #}
  {% do _create_index_if_table_exists('dims', 'dim_company', 'idx_dim_company_company_doc', 'company_id, document_version') %}
  {% do _create_index_if_table_exists('dims', 'dim_company', 'idx_dim_company_active_start_doc', 'company_id, is_active, start_at desc, document_version desc') %}
  {% do _create_index_if_table_exists('dims', 'dim_methodology', 'idx_dim_methodology_name', 'methodology_name') %}
  {% do _create_index_if_table_exists('dims', 'dim_credit_metric', 'idx_dim_credit_metric_name', 'metric_name') %}
  {% do _create_index_if_table_exists('dims', 'dim_industry_risk', 'idx_dim_industry_risk_join', 'industry_classification, industry_risk_score') %}
  {% do _create_index_if_table_exists('dims', 'dim_date', 'idx_dim_date_full_date', 'full_date') %}

  {# facts #}
  {% do _create_index_if_table_exists('facts', 'fct_rating_assessment', 'idx_fct_rating_assessment_join', 'record_hash, company_id, document_version') %}
  {% do _create_index_if_table_exists('facts', 'fct_rating_assessment', 'idx_fct_rating_assessment_company_doc', 'company_id, document_version') %}
  {% do _create_index_if_table_exists('facts', 'fct_rating_assessment', 'idx_fct_rating_assessment_date_key', 'source_modified_date_key') %}

  {% do _create_index_if_table_exists('facts', 'fct_credit_metric_value', 'idx_fct_credit_metric_join', 'record_hash, company_id, document_version') %}
  {% do _create_index_if_table_exists('facts', 'fct_credit_metric_value', 'idx_fct_credit_metric_metric_key', 'metric_key') %}
  {% do _create_index_if_table_exists('facts', 'fct_credit_metric_value', 'idx_fct_credit_metric_company_doc_year', 'company_id, document_version, year_label') %}

  {% do _create_index_if_table_exists('facts', 'bridge_assessment_methodology', 'idx_bridge_methodology_join', 'record_hash, company_id, document_version') %}
  {% do _create_index_if_table_exists('facts', 'bridge_assessment_methodology', 'idx_bridge_methodology_methodology_key', 'methodology_key') %}

  {% do _create_index_if_table_exists('facts', 'bridge_assessment_industry_risk', 'idx_bridge_industry_risk_join', 'record_hash, company_id, document_version') %}
  {% do _create_index_if_table_exists('facts', 'bridge_assessment_industry_risk', 'idx_bridge_industry_risk_key', 'industry_risk_key') %}
  {% do _create_index_if_table_exists('facts', 'bridge_assessment_industry_risk', 'idx_bridge_industry_risk_company_doc_ord', 'company_id, document_version, industry_risk_index') %}

  {% do _create_index_if_table_exists('facts', 'fct_company_timeseries', 'idx_fct_company_timeseries_lookup', 'company_id, column_name, metric_name, year_label, document_version, event_time') %}
  {% do _create_index_if_table_exists('facts', 'fct_company_timeseries', 'idx_fct_company_timeseries_root_lookup', 'company_id, column_name, document_version, event_time', "metric_name = 'value'") %}

  {# reports #}
  {% do _create_index_if_table_exists('reports', 'rep_company', 'idx_rep_company_active_lookup', 'company_id, is_active, start_at desc, document_version desc') %}
  {% do _create_index_if_table_exists('reports', 'rep_company', 'idx_rep_company_versions_lookup', 'company_id, document_version desc, start_at desc') %}
  {% do _create_index_if_table_exists('reports', 'rep_company', 'idx_rep_company_country', 'country') %}
  {% do _create_index_if_table_exists('reports', 'rep_company', 'idx_rep_company_sector', 'corporate_sector') %}
  {% do _create_index_if_table_exists('reports', 'rep_company', 'idx_rep_company_currency', 'reporting_currency') %}

  {# snapshots #}
  {% do _create_index_if_table_exists('snapshots', 'snap_company', 'idx_snap_company_latest', 'dbt_valid_to, company_id, source_modified_at_utc desc, dbt_valid_from desc, document_version desc') %}
  {% do _create_index_if_table_exists('snapshots', 'snap_company', 'idx_snap_company_company_date', 'company_id, source_modified_at_utc desc') %}
  {% do _create_index_if_table_exists('snapshots', 'snap_company', 'idx_snap_company_country', 'country') %}
  {% do _create_index_if_table_exists('snapshots', 'snap_company', 'idx_snap_company_sector', 'corporate_sector') %}
  {% do _create_index_if_table_exists('snapshots', 'snap_company', 'idx_snap_company_currency', 'reporting_currency') %}
{% endmacro %}
