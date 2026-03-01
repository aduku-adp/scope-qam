# Index Scripts

This directory contains idempotent SQL scripts to create indexes.

## What is automated
- dbt creates/maintains indexes after each run via `on-run-end` macro:
  - `modules/dbt_qam/macros/ensure_performance_indexes.sql`
- data-extraction ensures indexes on `raw` and `obs` tables during schema initialization.

## What is manual

- `raw.rating_assessments_history`
- all `obs` schema observability tables

Scripts:

- `01_indexes_raw_rating_assessments_history.sql`
- `02_indexes_obs_schema.sql`

Run all index scripts:

```bash
./tools/create_indexes.sh
```

Run example per file:

```bash
psql -h localhost -U postgres -d qam_db -f tools/sql/indexes/01_indexes_raw_rating_assessments_history.sql
psql -h localhost -U postgres -d qam_db -f tools/sql/indexes/02_indexes_obs_schema.sql
```
