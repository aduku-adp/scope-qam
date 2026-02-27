# scope-qam

Corporate credit rating data pipeline:
- extraction + validation: `modules/data-extraction`
- warehouse modeling: `modules/dbt_qam`
- orchestration: `modules/airflow`
- API: `modules/qam-api`

## One-command startup

```bash
docker compose up -d
```

## Key URLs

- FastAPI Swagger: `http://localhost:8000/docs`
- FastAPI Health: `http://localhost:8000/v1/health`
- Airflow UI: `http://localhost:8080`

## Sample API calls (10+)

```bash
# 1) health
curl -s http://localhost:8000/v1/health

# 2) companies (latest active)
curl -s http://localhost:8000/v1/companies

# 3) one company
curl -s http://localhost:8000/v1/companies/company_a

# 4) company versions
curl -s http://localhost:8000/v1/companies/company_a/versions

# 5) company history
curl -s "http://localhost:8000/v1/companies/company_a/history"

# 6) company history filtered
curl -s "http://localhost:8000/v1/companies/company_a/history?series_type=credit_metric&series_name=scope_adjusted_debt_ebitda&year_label=2025E"

# 7) compare companies (latest)
curl -s "http://localhost:8000/v1/companies/compare?company_ids=company_a,company_b"

# 8) compare companies (point-in-time)
curl -s "http://localhost:8000/v1/companies/compare?company_ids=company_a,company_b&as_of_date=2026-02-25T00:00:00Z"

# 9) snapshots list
curl -s "http://localhost:8000/v1/snapshots?country=Federal%20Republic%20of%20Germany"

# 10) snapshots latest
curl -s http://localhost:8000/v1/snapshots/latest

# 11) uploads list
curl -s http://localhost:8000/v1/uploads

# 12) uploads stats
curl -s http://localhost:8000/v1/uploads/stats
```

## Example response snippets

```json
{
  "status": "OK",
  "request_uid": "8e8f4e5b-a6de-4fb0-9df9-a4dbcb26f211",
  "data": []
}
```

```json
{
  "status": "OK",
  "request_uid": "6efcc248-60e0-4a37-87e7-2bb9ab91e3bb",
  "data": {
    "healthy": true,
    "database_ok": true,
    "corporates_dir_ok": true,
    "corporates_dir_path": "/data/corporates",
    "corporates_files_count": 5,
    "database_message": "ok",
    "corporates_dir_message": "ok"
  }
}
```

## Data quality report example

From `obs.data_quality_rule_results`:

```sql
select run_id, scope, rule_id, severity, status, violations, details, created_at
from obs.data_quality_rule_results
order by created_at desc
limit 20;
```

Example row:

```json
{
  "rule_id": "industry_weight_sum",
  "severity": "error",
  "status": "passed",
  "violations": 0,
  "details": null
}
```

## Pipeline run log example

Printed by extraction pipeline and stored in `obs.pipeline_runs`:

```json
{
  "run_id": "6b909768-3edf-45b2-b2f7-1d87703c92a0",
  "pipeline_name": "extract_company_history",
  "started_at": "2026-02-27T10:12:44.304889+00:00",
  "duration": 1.92,
  "files_discovered": 5,
  "files_processed": 5,
  "rows_inserted": 2,
  "rows_skipped": 3,
  "extraction_failures": 1,
  "validation_failures": 1,
  "load_failures": 0,
  "warnings": 2,
  "errors": 2,
  "completeness_rate": 0.8,
  "validity_rate": 0.6,
  "status": "failed"
}
```
