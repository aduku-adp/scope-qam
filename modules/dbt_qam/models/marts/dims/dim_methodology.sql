{{
  config(
    materialized='incremental',
    unique_key='methodology_key',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
  )
}}

with base as (
    select distinct methodology_name
    from {{ ref('stg_rating_methodologies') }}
)
select
    md5(methodology_name) as methodology_key,
    methodology_name
from base
