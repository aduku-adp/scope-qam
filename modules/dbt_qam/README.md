# dbt_qam Module

Warehouse transformations for the QAM pipeline (staging, marts, reports, snapshots).

## Model lineage

![dbt model lineage graph](/images/model_lineage_graph.png)

## Scope

- Source: `raw.rating_assessments_history`
- Target schemas:
  - `staging`
  - `dims`
  - `facts`
  - `reports`
  - `snapshots`
- Primary API-facing reporting model:
  - `reports.rep_company`
- Time-series model:
  - `facts.fct_company_timeseries`
- Snapshot model:
  - `snapshots.snap_company` (dbt snapshot, timestamp strategy)

## Project layout

- `models/staging`: raw normalization/explosions.
- `models/marts/dims`: dimensions (company/date/methodology/industry risk/credit metric).
- `models/marts/facts`: facts + bridge tables + unified time series.
- `models/reports`: denormalized reporting layer.
- `snapshots`: dbt snapshot definitions.
- `macros`:
  - schema naming
  - performance index creation (`on-run-end`)

## Configuration

Project config: [`dbt_project.yml`](/modules/dbt_qam/dbt_project.yml)

Profiles: [`profiles.yml`](/modules/dbt_qam/profiles.yml)

- `target: dev` for local runs (`PG_HOST` default `localhost`)
- `target: airflow` for container/Airflow runs (`PG_HOST` default `postgres`)

Used env vars:

- `PG_HOST`
- `PG_PORT`
- `PG_USER`
- `PG_PASSWORD`
- `DB_NAME`

## Run locally

From module directory:

```bash
cd modules/dbt_qam
dbt debug --profiles-dir .
dbt run --profiles-dir . --target dev
dbt test --profiles-dir . --target dev
dbt snapshot --profiles-dir . --target dev --select snap_company
dbt test --profiles-dir . --target dev --select resource_type:snapshot
```

## Serve dbt docs

`dbt docs serve` requires generated artifacts (`manifest.json` and `catalog.json`).

From `scope-qam/modules/dbt_qam`:

```bash
dbt docs generate --profiles-dir . --target dev
dbt docs serve --profiles-dir . --target dev --port 8001
```

## Run in Airflow/container context

```bash
cd /opt/airflow/repo/modules/dbt_qam
dbt run --profiles-dir . --target airflow
dbt test --profiles-dir . --target airflow --exclude resource_type:snapshot
dbt snapshot --profiles-dir . --target airflow --select snap_company
dbt test --profiles-dir . --target airflow --select resource_type:snapshot
```

## Incremental strategy

All table/fact/report models are configured incremental with:

- `materialized='incremental'`
- `incremental_strategy='delete+insert'`
- stable unique keys
- `on_schema_change='sync_all_columns'`

## Performance

At end of each dbt run, macro `ensure_performance_indexes()` is executed via `on-run-end`.

Macro file:

- [`ensure_performance_indexes.sql`](/modules/dbt_qam/macros/ensure_performance_indexes.sql)

Additional optional partition scripts:

- [`tools/sql/partitions`](/tools/sql/partitions)
- [`tools/create_partitions.sh`](/tools/create_partitions.sh)

Additional optional indexing scripts:

- [`tools/sql/indexes`](/tools/sql/indexes)
- [`tools/create_indexes.sh`](/tools/create_indexes.sh)

## Key models

- Staging:
  - `stg_rating_assessments_history`
  - `stg_rating_methodologies`
  - `stg_industry_risks`
  - `stg_credit_metrics`
- Dims:
  - `dim_company` (SCD-like attributes per version)
  - `dim_date`
  - `dim_methodology`
  - `dim_industry_risk`
  - `dim_credit_metric`
- Facts:
  - `fct_rating_assessment`
  - `fct_credit_metric_value`
  - `bridge_assessment_methodology`
  - `bridge_assessment_industry_risk`
  - `fct_company_timeseries`
- Reports:
  - `rep_company`
- Snapshot:
  - `snap_company`

## Data contracts/tests

Schema YAML docs and tests:

- [`models/staging/schema.yml`](/modules/dbt_qam/models/staging/schema.yml)
- [`models/marts/schema.yml`](/modules/dbt_qam/models/marts/schema.yml)
- [`models/reports/schema.yml`](/modules/dbt_qam/models/reports/schema.yml)
- [`snapshots/schema.yml`](/modules/dbt_qam/snapshots/schema.yml)
