{% macro generate_schema_name(custom_schema_name, node) -%}
    {# Keep explicit custom schemas (staging/dims/facts/reports/snapshots) unchanged. #}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
