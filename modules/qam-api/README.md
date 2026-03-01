# qam-api Module

FastAPI service exposing company, snapshot, upload-audit, and health endpoints over the QAM warehouse.

## Scope

- Framework: FastAPI + Pydantic
- DB access: psycopg2 (readonly query services)
- API base path: `/v1`
- Default container port: `8080` (mapped to host `8000` by docker compose)

Swagger:

- `http://localhost:8000/docs`

## Folder structure

- `src/`
  - `application.py`: app wiring + service/provider DI.
  - `main.py`: uvicorn entrypoint.
  - `api/company`: company endpoints/models/service.
  - `api/snapshot`: snapshot endpoints/models/service.
  - `api/upload`: upload audit endpoints/models/service.
  - `api/health`: health endpoint.
  - `api/providers`: SQL providers.
  - `helpers`: constants, formatter, shared exceptions.
- `e2e-tests/`: integration tests against running service.
- `Dockerfile`: runtime image definition.
- `requirements.txt`: Python dependencies.

## Endpoints

### Health

- `GET /v1/health`

### Company

- `GET /v1/companies`
- `GET /v1/companies/{company_id}`
- `GET /v1/companies/{company_id}/versions`
- `GET /v1/companies/{company_id}/history`
  - Required query param: `column_name`
  - Optional: `metric_name`, `year_label`
- `GET /v1/companies/compare`
  - Required query param: `company_ids` (comma-separated)
  - Optional: `as_of_date`
  - Returns diffs only

### Snapshot

- `GET /v1/snapshots`
  - Optional filters: `company_id`, `from_date`, `to_date`, `sector`, `country`, `currency`
- `GET /v1/snapshots/latest`
- `GET /v1/snapshots/{snapshot_id}`

### Upload audit

- `GET /v1/uploads`
- `GET /v1/uploads/stats`
- `GET /v1/uploads/{upload_id}/details`
- `GET /v1/uploads/{upload_id}/file`

## Configuration

Environment variables used:

- `SERVICE_URL` (tests/helpers)
- `IDENTITY` (optional header in e2e connector)
- `PG_HOST`
- `PG_PORT`
- `PG_USER`
- `PG_PASSWORD`
- `DB_NAME`
- `UPLOAD_FILE_SEARCH_DIRS` (comma-separated fallback locations for upload file download)
- `UPLOAD_REPO_MOUNT_ROOT` (optional path translation from extractor container path)

Local env examples:

- [`modules/qam-api/.env`](/modules/qam-api/.env)
- [`modules/qam-api/test_env.sh`](/modules/qam-api/test_env.sh)

## Run locally (without Docker)

```bash
cd modules/qam-api/src
python main.py
```

Service:

- `http://localhost:8000` (when running directly)

## Run with Docker Compose

From repository root:

```bash
docker compose up -d qam-api
```

Service:

- `http://localhost:8000`

## Build local API image

```bash
./tools/build_qam_api.sh
```

Script:

- [`tools/build_qam_api.sh`](/tools/build_qam_api.sh)

## Tests

### Unit tests

```bash
pytest -q modules/qam-api/src
```

### E2E tests

Requires running API + database with data loaded.

```bash
pytest -q modules/qam-api/e2e-tests
```

Primary e2e suite:

- [`company_test.py`](/modules/qam-api/e2e-tests/company_test.py)

## Data dependencies

The API reads from:

- `reports.rep_company`
- `facts.fct_company_timeseries` (company history endpoint)
- `snapshots.snap_company`
- observability tables under `obs.*` for upload endpoints

