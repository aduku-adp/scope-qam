# Data Extraction Module

Extracts company assessment data from Excel `MASTER` sheets, validates payloads, and loads `raw.rating_assessments_history` with observability events.

## Scope

- Input files: `./data/corporates/*.xlsm|*.xlsx`
- Sheet processed: `MASTER` only
- Pipeline stages:
  - Extract
  - Schema validation (Pydantic)
  - Business-rule validation (YAML-driven)
  - Load to Postgres
  - Observability logging (pipeline runs, file events, data quality, lineage, state)

Entrypoint: [`extract_company_history.py`](/modules/data-extraction/extract_company_history.py)

## Folder structure

- `extract_company_history.py`: CLI entrypoint and backward-compatible helpers.
- `pipeline.py`: orchestrator (`CompanyExtractionPipeline`).
- `excel_extractor.py`: MASTER sheet parser.
- `validation_models.py`: strict Pydantic schema validation.
- `business_rules.py`: dataset-level business rules.
- `business_rules.yml`: business rule config.
- `postgres_repository.py`: DDL + DML access layer.
- `config.py`: env and runtime config loading.
- `tests/`: unit tests.

## Runtime configuration

The module reads DB config from environment variables first, then `./.env` fallback.

Required/used variables:

- `PG_HOST` (default: `postgres` in module defaults)
- `PG_PORT` (default: `5432`)
- `PG_USER` (default: `postgres`)
- `PG_PASSWORD` (default: `postgres`)
- `DB_NAME` or `PG_DATABASE` (default: `qam_db`)

Runtime defaults are defined in [`config.py`](/modules/data-extraction/config.py):

- `data_dir`: `./data/corporates`
- `rules_file`: `modules/data-extraction/business_rules.yml`
- `target_sheet_name`: `MASTER`

## Run locally

From repo root:

```bash
python modules/data-extraction/extract_company_history.py
```

Or from module directory:

```bash
cd modules/data-extraction
python extract_company_history.py
```

## Incremental and idempotency behavior

- Files are discovered from `data/corporates`.
- Processing order: ascending `source_modified_at_utc`.
- Incremental cutoff:
  - uses max source timestamp from raw data and pipeline state.
  - only files with `source_modified_at_utc >= cutoff` are considered.
- Idempotency:
  - payload hash (`record_hash`) is used to skip duplicates.
  - duplicate skips are not inserted as file error/warning events.
- Versioning:
  - `document_version` increments per `company_id`.

## Observability tables (written by this module)

- `obs.pipeline_runs`
- `obs.file_ingestion_events`
- `obs.data_quality_rule_results`
- `obs.lineage_events`
- `obs.pipeline_state`
- `obs.processed_files`

Raw target:

- `raw.rating_assessments_history`

## Validation

### Schema validation (strict)

- Required fields present.
- Primitive types enforced (numeric/text/date).
- Nested objects and list structures validated.

### Business rules

Defined in `business_rules.yml`, evaluated by `BusinessRuleEngine`:

- Industry weight totals (with tolerance).
- Allowed score scales.
- Credit metric year/value logic.
- Suspicious/outlier checks.

Validation failures are written to observability tables with per-file and per-rule results.

## Tests

Run:

```bash
pytest -q modules/data-extraction/tests
```

Test files:

- [`extract_company_history_test.py`](/modules/data-extraction/tests/extract_company_history_test.py)
- [`validation_models_test.py`](/modules/data-extraction/tests/validation_models_test.py)
- [`business_rules_test.py`](/modules/data-extraction/tests/business_rules_test.py)

## Common failure modes

- `BadZipFile: File is not a zip file`
  - Non-Excel or corrupted file in `data/corporates`.
- DB connection refused
  - Wrong host from runtime context (for Docker use service host `postgres`, not `localhost`).
- Validation errors for metric values/types
  - Source file has incompatible cell types vs strict schema.

