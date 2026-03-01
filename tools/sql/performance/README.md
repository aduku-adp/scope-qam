# Performance DDL

This directory contains SQL scripts to improve warehouse query performance.

## What is automated
- dbt creates/maintains indexes after each run via `on-run-end` macro:
  - `modules/dbt_qam/macros/ensure_performance_indexes.sql`
- data-extraction ensures indexes on `raw` and `obs` tables during schema initialization.

## What is manual
Partition migrations are one-time, maintenance-window operations:
1. `01_partition_raw_rating_assessments_history.sql`
2. `02_partition_facts_company_timeseries.sql`
3. `03_partition_snapshots_snap_company.sql`

Validate row counts and API/dbt behavior before dropping `_old` tables.
