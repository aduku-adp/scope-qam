# scope-qam

Corporate credit rating data platform with:
- Python extraction + validation pipeline
- dbt warehouse transformations + snapshots
- Airflow orchestration
- FastAPI analytics and audit endpoints

## Module documentation

- Data extraction: [modules/data-extraction/README.md](/modules/data-extraction/README.md)
- dbt transformations: [modules/dbt_qam/README.md](/modules/dbt_qam/README.md)
- Airflow orchestration: [modules/airflow/README.md](/modules/airflow/README.md)
- API service: [modules/qam-api/README.md](/modules/qam-api/README.md)


## Architecture Diagram

![QAM architecture diagram](/images/qam-architecture.png)

## Stack startup

Follow this process to startup your stack correctly.

### 0. Clone the project
- Clone the project
```bash
git clone git@github.com:aduku-adp/scope-qam.git
```

- Create an .env file from provided template
```bash
cd scope-qam
cp .env-template .env
```


### 1. One-command stack startup

```bash
cd tools/
./clean_deploy_stack.sh
```

## Key URLs

- FastAPI Swagger: `http://localhost:8000/docs`
- FastAPI Health: `http://localhost:8000/v1/health`
- Airflow UI: `http://localhost:8080`
- dbt docs (if served): `http://localhost:8001`


### 2. Trigger a data ingestion via airflow

- Connect to airflow UI with default airflow credentials:
  - Username: airflow
  - Password: airflow

- Run the dag: `company_etl_pipeline`


### 3. Apply partition and index scripts

```bash
./tools/create_partitions.sh
./tools/create_indexes.sh
```


### 4. Go to FastAPI Swagger: `http://localhost:8000/docs`


## Data location

Corporate input files are expected in:

- `data/corporates/*.xlsm|*.xlsx`


## dbt docs

From `scope-qam/modules/dbt_qam`:

```bash
dbt docs generate --profiles-dir . --target dev
dbt docs serve --profiles-dir . --target dev --port 8001
```


## Sample API calls (10+)

### 1) health

- request:
```bash
curl -s http://localhost:8000/v1/health
```

- response:
```json
{
  "data": {
    "healthy": true,
    "database_ok": true,
    "corporates_dir_ok": true,
    "corporates_dir_path": "/data/corporates",
    "corporates_files_count": 9,
    "database_message": "ok",
    "corporates_dir_message": "ok"
  },
  "request_uid": "4d7fef9c-c914-4e03-afad-ba65afb6caca",
  "status": "OK"
}
```

### 2) companies (latest active)

- request:
```bash
curl -s http://localhost:8000/v1/companies
```

- response:
```json
{
{
  "data": [
    {
      "rep_company_key": "8e484a1d5f18d66b2d2304a4b4c1671b",
      "company_id": "company_a",
      "company_name": "Company A",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "IFRS",
      "fiscal_year_end": "December",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "BBB",
      "industry_weight": "1.0",
      "segmentation_criteria": "EBITDA contribution",
      "rating_methodologies_applied": "General Corporate Rating Methodology",
      "document_version": 2,
      "start_at": "2026-02-25T23:54:55.274839Z",
      "is_active": true,
      "source_modified_date_key": 20260225,
      "source_modified_date": "2026-02-25",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
      "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
      "ingested_at": "2026-03-01T06:21:32.651154Z",
      "business_risk_score": "B",
      "financial_risk_score": "CC",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "B+",
      "market_share": "B+",
      "diversification": "B+",
      "operating_profitability": "B",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 23
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 9
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    },
    {
      "rep_company_key": "f6b65a80f13f3a8f44764027cdd5b02b",
      "company_id": "company_b",
      "company_name": "Company B",
      "country": "Swiss Confederation",
      "corporate_sector": "Automobiles & Parts",
      "reporting_currency": "CHF",
      "accounting_principles": "IFRS",
      "fiscal_year_end": "March",
      "industry_classification": "Automotive Suppliers | Automotive and Commercial Vehicle Manufacturers",
      "industry_risk_score": "BBB | BB",
      "industry_weight": "0.85 | 0.15",
      "segmentation_criteria": "EBITDA contribution",
      "rating_methodologies_applied": "Automotive and Commercial Vehicle Manufacturers Rating Methodology",
      "document_version": 4,
      "start_at": "2026-03-01T07:16:29.318003Z",
      "is_active": true,
      "source_modified_date_key": 20260301,
      "source_modified_date": "2026-03-01",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_3.xlsm",
      "source_modified_at_utc": "2026-03-01T07:16:29.318003Z",
      "ingested_at": "2026-03-01T07:16:40.542763Z",
      "business_risk_score": "BBB-",
      "financial_risk_score": "BB",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "A+",
      "market_share": "BBB+",
      "diversification": "A-",
      "operating_profitability": "BB+",
      "sector_company_specific_factors_1": "BBB+",
      "leverage": "BB+",
      "interest_cover": "BBB+",
      "cash_flow_cover": "A-",
      "liquidity_adjustment_notches": 1,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        }
      ]
    },
    {
      "rep_company_key": "3fb5f99023cd35057d952dd5ae1f0bfd",
      "company_id": "company_c",
      "company_name": "Company C",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "US-GAAP",
      "fiscal_year_end": "November",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "A",
      "industry_weight": "1.0",
      "segmentation_criteria": "Revenue contribution",
      "rating_methodologies_applied": "Consumer Products Rating Methodology | General Corporate Rating Methodology",
      "document_version": 1,
      "start_at": "2026-02-27T02:38:29.725072Z",
      "is_active": true,
      "source_modified_date_key": 20260227,
      "source_modified_date": "2026-02-27",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_C_1.xlsm",
      "source_modified_at_utc": "2026-02-27T02:38:29.725072Z",
      "ingested_at": "2026-03-01T06:21:32.785770Z",
      "business_risk_score": "A+",
      "financial_risk_score": "C",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "A+",
      "market_share": "BB-",
      "diversification": "A+",
      "operating_profitability": "BB-",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    }
  ],
  "request_uid": "719ad9cc-2449-4adf-b50f-064143424c5c",
  "status": "OK"
}
}
```

### 3) one company

- request:
```bash
curl -s http://localhost:8000/v1/companies/company_a
```

- response:
```json
{
  "data": {
    "rep_company_key": "8e484a1d5f18d66b2d2304a4b4c1671b",
    "company_id": "company_a",
    "company_name": "Company A",
    "country": "Federal Republic of Germany",
    "corporate_sector": "Personal & Household Goods",
    "reporting_currency": "EUR",
    "accounting_principles": "IFRS",
    "fiscal_year_end": "December",
    "industry_classification": "Consumer Products: Non-Discretionary",
    "industry_risk_score": "BBB",
    "industry_weight": "1.0",
    "segmentation_criteria": "EBITDA contribution",
    "rating_methodologies_applied": "General Corporate Rating Methodology",
    "document_version": 2,
    "start_at": "2026-02-25T23:54:55.274839Z",
    "is_active": true,
    "source_modified_date_key": 20260225,
    "source_modified_date": "2026-02-25",
    "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
    "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
    "ingested_at": "2026-03-01T06:21:32.651154Z",
    "business_risk_score": "B",
    "financial_risk_score": "CC",
    "blended_industry_risk_profile": "A",
    "competitive_positioning": "B+",
    "market_share": "B+",
    "diversification": "B+",
    "operating_profitability": "B",
    "sector_company_specific_factors_1": "B-",
    "leverage": "CCC",
    "interest_cover": "B-",
    "cash_flow_cover": "CCC",
    "liquidity_adjustment_notches": -2,
    "credit_metrics": [
      {
        "locked": true,
        "year_label": "2018",
        "is_estimate": false,
        "metric_name": "liquidity",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2019",
        "is_estimate": false,
        "metric_name": "liquidity",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2020",
        "is_estimate": false,
        "metric_name": "liquidity",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2021",
        "is_estimate": false,
        "metric_name": "liquidity",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2022",
        "is_estimate": false,
        "metric_name": "liquidity",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2023",
        "is_estimate": false,
        "metric_name": "liquidity",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2024",
        "is_estimate": false,
        "metric_name": "liquidity",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2025E",
        "is_estimate": true,
        "metric_name": "liquidity",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2026E",
        "is_estimate": true,
        "metric_name": "liquidity",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2027E",
        "is_estimate": true,
        "metric_name": "liquidity",
        "metric_value": 23
      },
      {
        "locked": true,
        "year_label": "2018",
        "is_estimate": false,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2019",
        "is_estimate": false,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2020",
        "is_estimate": false,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2021",
        "is_estimate": false,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2022",
        "is_estimate": false,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2023",
        "is_estimate": false,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2024",
        "is_estimate": false,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2025E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2026E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2027E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_debt_ebitda",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2018",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2019",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2020",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2021",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2022",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2023",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2024",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2025E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2026E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2027E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_ebitda_interest_cover",
        "metric_value": 18.491
      },
      {
        "locked": true,
        "year_label": "2018",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 22
      },
      {
        "locked": true,
        "year_label": "2019",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 22
      },
      {
        "locked": true,
        "year_label": "2020",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 22
      },
      {
        "locked": true,
        "year_label": "2021",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2022",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2023",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2024",
        "is_estimate": false,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 29
      },
      {
        "locked": true,
        "year_label": "2025E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 29
      },
      {
        "locked": true,
        "year_label": "2026E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 29
      },
      {
        "locked": true,
        "year_label": "2027E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_ffo_debt",
        "metric_value": 9
      },
      {
        "locked": true,
        "year_label": "2018",
        "is_estimate": false,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2019",
        "is_estimate": false,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2020",
        "is_estimate": false,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2021",
        "is_estimate": false,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 21.532
      },
      {
        "locked": true,
        "year_label": "2022",
        "is_estimate": false,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2023",
        "is_estimate": false,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2024",
        "is_estimate": false,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2025E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2026E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2027E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_focf_debt",
        "metric_value": 4.862
      },
      {
        "locked": true,
        "year_label": "2018",
        "is_estimate": false,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2019",
        "is_estimate": false,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2020",
        "is_estimate": false,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2021",
        "is_estimate": false,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2022",
        "is_estimate": false,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 36.8
      },
      {
        "locked": true,
        "year_label": "2023",
        "is_estimate": false,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": null
      },
      {
        "locked": true,
        "year_label": "2024",
        "is_estimate": false,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2025E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2026E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 27.329
      },
      {
        "locked": true,
        "year_label": "2027E",
        "is_estimate": true,
        "metric_name": "scope_adjusted_loan_value",
        "metric_value": 4.862
      }
    ]
  },
  "request_uid": "a092877e-6b46-429b-9ad6-cf3926bad5f4",
  "status": "OK"
}
```

### 4) company versions

- request:
```bash
curl -s http://localhost:8000/v1/companies/company_a/versions
```

- response:
```json
{
  "data": [
    {
      "rep_company_key": "8e484a1d5f18d66b2d2304a4b4c1671b",
      "company_id": "company_a",
      "company_name": "Company A",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "IFRS",
      "fiscal_year_end": "December",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "BBB",
      "industry_weight": "1.0",
      "segmentation_criteria": "EBITDA contribution",
      "rating_methodologies_applied": "General Corporate Rating Methodology",
      "document_version": 2,
      "start_at": "2026-02-25T23:54:55.274839Z",
      "is_active": true,
      "source_modified_date_key": 20260225,
      "source_modified_date": "2026-02-25",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
      "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
      "ingested_at": "2026-03-01T06:21:32.651154Z",
      "business_risk_score": "B",
      "financial_risk_score": "CC",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "B+",
      "market_share": "B+",
      "diversification": "B+",
      "operating_profitability": "B",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 23
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 9
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    },
    {
      "rep_company_key": "312afd5203df7ea88cb848ae10805ea6",
      "company_id": "company_a",
      "company_name": "Company A",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "IFRS",
      "fiscal_year_end": "December",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "A",
      "industry_weight": "1.0",
      "segmentation_criteria": "EBITDA contribution",
      "rating_methodologies_applied": "Consumer Products Rating Methodology | General Corporate Rating Methodology",
      "document_version": 1,
      "start_at": "2026-02-24T09:17:38.844473Z",
      "end_at": "2026-02-25T23:54:55.274839Z",
      "is_active": false,
      "source_modified_date_key": 20260224,
      "source_modified_date": "2026-02-24",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_1.xlsm",
      "source_modified_at_utc": "2026-02-24T09:17:38.844473Z",
      "ingested_at": "2026-03-01T06:21:32.398705Z",
      "business_risk_score": "B+",
      "financial_risk_score": "C",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "B+",
      "market_share": "BB-",
      "diversification": "B+",
      "operating_profitability": "BB-",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    }
  ],
  "request_uid": "dfd6cf2b-a079-49b2-8574-bf50b9a8f423",
  "status": "OK"
}
```

### 5) company history (column_name required)

- request:
```bash
curl -s "http://localhost:8000/v1/companies/company_a/history?column_name=industry_risk_score"
```

- response:
```json
{
  "data": [
    {
      "timeseries_key": "557101ee2846778bddaca35e799ba6e0",
      "company_id": "company_a",
      "document_version": 1,
      "event_time": "2026-02-24T09:17:38.844473Z",
      "column_name": "industry_risk_score",
      "metric_name": "value",
      "series_value": "A"
    },
    {
      "timeseries_key": "3435424b2766520154040588c2b211b3",
      "company_id": "company_a",
      "document_version": 2,
      "event_time": "2026-02-25T23:54:55.274839Z",
      "column_name": "industry_risk_score",
      "metric_name": "value",
      "series_value": "BBB"
    }
  ],
  "request_uid": "6f24aa90-e5f1-443a-884c-ebf3e4d9f01b",
  "status": "OK"
}
```

### 6) company history filtered (3 levels)

- request:
```bash
curl -s "http://localhost:8000/v1/companies/company_a/history?column_name=credit_metrics&metric_name=scope_adjusted_debt_ebitda&year_label=2025E"
```

- response:
```json
{
  "data": [
    {
      "timeseries_key": "d8732b98bd2df358efa6283dc74f9eff",
      "company_id": "company_a",
      "document_version": 1,
      "event_time": "2026-02-24T09:17:38.844473Z",
      "column_name": "credit_metrics",
      "metric_name": "scope_adjusted_debt_ebitda",
      "series_value": "36.8",
      "year_label": "2025E",
      "is_estimate": true
    },
    {
      "timeseries_key": "db1b3020f58ac53fbae438043b19c370",
      "company_id": "company_a",
      "document_version": 2,
      "event_time": "2026-02-25T23:54:55.274839Z",
      "column_name": "credit_metrics",
      "metric_name": "scope_adjusted_debt_ebitda",
      "series_value": "36.8",
      "year_label": "2025E",
      "is_estimate": true
    }
  ],
  "request_uid": "0be87b77-0926-42ca-b4d4-e079f13b97ca",
  "status": "OK"
}
```

### 7) compare companies (latest)

- request:
```bash
curl -s "http://localhost:8000/v1/companies/compare?company_ids=company_a,company_b"
```

- response:
```json
{
  "data": [
    {
      "column": "company_id",
      "values_by_company_id": {
        "company_a": "company_a",
        "company_b": "company_b"
      }
    },
    {
      "column": "company_name",
      "values_by_company_id": {
        "company_a": "Company A",
        "company_b": "Company B"
      }
    },
    {
      "column": "country",
      "values_by_company_id": {
        "company_a": "Federal Republic of Germany",
        "company_b": "Swiss Confederation"
      }
    },
    {
      "column": "corporate_sector",
      "values_by_company_id": {
        "company_a": "Personal & Household Goods",
        "company_b": "Automobiles & Parts"
      }
    },
    {
      "column": "reporting_currency",
      "values_by_company_id": {
        "company_a": "EUR",
        "company_b": "CHF"
      }
    },
    {
      "column": "fiscal_year_end",
      "values_by_company_id": {
        "company_a": "December",
        "company_b": "March"
      }
    },
    {
      "column": "industry_classification",
      "values_by_company_id": {
        "company_a": "Consumer Products: Non-Discretionary",
        "company_b": "Automotive Suppliers | Automotive and Commercial Vehicle Manufacturers"
      }
    },
    {
      "column": "industry_risk_score",
      "values_by_company_id": {
        "company_a": "BBB",
        "company_b": "BBB | BB"
      }
    },
    {
      "column": "industry_weight",
      "values_by_company_id": {
        "company_a": "1.0",
        "company_b": "0.85 | 0.15"
      }
    },
    {
      "column": "rating_methodologies_applied",
      "values_by_company_id": {
        "company_a": "General Corporate Rating Methodology",
        "company_b": "Automotive and Commercial Vehicle Manufacturers Rating Methodology"
      }
    },
    {
      "column": "document_version",
      "values_by_company_id": {
        "company_a": 2,
        "company_b": 4
      }
    },
    {
      "column": "start_at",
      "values_by_company_id": {
        "company_a": "2026-02-25T23:54:55.274839Z",
        "company_b": "2026-03-01T07:16:29.318003Z"
      }
    },
    {
      "column": "source_modified_date_key",
      "values_by_company_id": {
        "company_a": 20260225,
        "company_b": 20260301
      }
    },
    {
      "column": "source_modified_date",
      "values_by_company_id": {
        "company_a": "2026-02-25",
        "company_b": "2026-03-01"
      }
    },
    {
      "column": "source_file_path",
      "values_by_company_id": {
        "company_a": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
        "company_b": "/opt/airflow/repo/data/corporates/corporates_B_3.xlsm"
      }
    },
    {
      "column": "source_modified_at_utc",
      "values_by_company_id": {
        "company_a": "2026-02-25T23:54:55.274839Z",
        "company_b": "2026-03-01T07:16:29.318003Z"
      }
    },
    {
      "column": "ingested_at",
      "values_by_company_id": {
        "company_a": "2026-03-01T06:21:32.651154Z",
        "company_b": "2026-03-01T07:16:40.542763Z"
      }
    },
    {
      "column": "business_risk_score",
      "values_by_company_id": {
        "company_a": "B",
        "company_b": "BBB-"
      }
    },
    {
      "column": "financial_risk_score",
      "values_by_company_id": {
        "company_a": "CC",
        "company_b": "BB"
      }
    },
    {
      "column": "competitive_positioning",
      "values_by_company_id": {
        "company_a": "B+",
        "company_b": "A+"
      }
    },
    {
      "column": "market_share",
      "values_by_company_id": {
        "company_a": "B+",
        "company_b": "BBB+"
      }
    },
    {
      "column": "diversification",
      "values_by_company_id": {
        "company_a": "B+",
        "company_b": "A-"
      }
    },
    {
      "column": "operating_profitability",
      "values_by_company_id": {
        "company_a": "B",
        "company_b": "BB+"
      }
    },
    {
      "column": "sector_company_specific_factors_1",
      "values_by_company_id": {
        "company_a": "B-",
        "company_b": "BBB+"
      }
    },
    {
      "column": "leverage",
      "values_by_company_id": {
        "company_a": "CCC",
        "company_b": "BB+"
      }
    },
    {
      "column": "interest_cover",
      "values_by_company_id": {
        "company_a": "B-",
        "company_b": "BBB+"
      }
    },
    {
      "column": "cash_flow_cover",
      "values_by_company_id": {
        "company_a": "CCC",
        "company_b": "A-"
      }
    },
    {
      "column": "liquidity_adjustment_notches",
      "values_by_company_id": {
        "company_a": -2,
        "company_b": 1
      }
    },
    {
      "column": "credit_metrics",
      "values_by_company_id": {
        "company_a": [
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 23
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 22
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 22
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 22
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 29
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 29
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 29
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 9
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": null
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 4.862
          }
        ],
        "company_b": [
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": null
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          }
        ]
      }
    }
  ],
  "request_uid": "01ea295d-930f-4995-a340-1dd88ffecb50",
  "status": "OK"
}
```

### 8) compare companies (point-in-time)

- request:
```bash
curl -s "http://localhost:8000/v1/companies/compare?company_ids=company_a,company_b&as_of_date=2026-02-25T00:00:00Z"
```

- response:
```json
{
  "data": [
    {
      "column": "company_id",
      "values_by_company_id": {
        "company_a": "company_a",
        "company_b": "company_b"
      }
    },
    {
      "column": "company_name",
      "values_by_company_id": {
        "company_a": "Company A",
        "company_b": "Company B"
      }
    },
    {
      "column": "country",
      "values_by_company_id": {
        "company_a": "Federal Republic of Germany",
        "company_b": "Swiss Confederation"
      }
    },
    {
      "column": "corporate_sector",
      "values_by_company_id": {
        "company_a": "Personal & Household Goods",
        "company_b": "Automobiles & Parts"
      }
    },
    {
      "column": "reporting_currency",
      "values_by_company_id": {
        "company_a": "EUR",
        "company_b": "CHF"
      }
    },
    {
      "column": "fiscal_year_end",
      "values_by_company_id": {
        "company_a": "December",
        "company_b": "March"
      }
    },
    {
      "column": "industry_classification",
      "values_by_company_id": {
        "company_a": "Consumer Products: Non-Discretionary",
        "company_b": "Automotive Suppliers | Automotive and Commercial Vehicle Manufacturers"
      }
    },
    {
      "column": "industry_risk_score",
      "values_by_company_id": {
        "company_a": "A",
        "company_b": "BBB | BB"
      }
    },
    {
      "column": "industry_weight",
      "values_by_company_id": {
        "company_a": "1.0",
        "company_b": "0.15 | 0.85"
      }
    },
    {
      "column": "rating_methodologies_applied",
      "values_by_company_id": {
        "company_a": "Consumer Products Rating Methodology | General Corporate Rating Methodology",
        "company_b": "Automotive and Commercial Vehicle Manufacturers Rating Methodology"
      }
    },
    {
      "column": "start_at",
      "values_by_company_id": {
        "company_a": "2026-02-24T09:17:38.844473Z",
        "company_b": "2026-02-24T09:17:38.844634Z"
      }
    },
    {
      "column": "end_at",
      "values_by_company_id": {
        "company_a": "2026-02-25T23:54:55.274839Z",
        "company_b": "2026-02-28T10:32:36.570924Z"
      }
    },
    {
      "column": "source_file_path",
      "values_by_company_id": {
        "company_a": "/opt/airflow/repo/data/corporates/corporates_A_1.xlsm",
        "company_b": "/opt/airflow/repo/data/corporates/corporates_B_1.xlsm"
      }
    },
    {
      "column": "source_modified_at_utc",
      "values_by_company_id": {
        "company_a": "2026-02-24T09:17:38.844473Z",
        "company_b": "2026-02-24T09:17:38.844634Z"
      }
    },
    {
      "column": "ingested_at",
      "values_by_company_id": {
        "company_a": "2026-03-01T06:21:32.398705Z",
        "company_b": "2026-03-01T06:21:32.545471Z"
      }
    },
    {
      "column": "business_risk_score",
      "values_by_company_id": {
        "company_a": "B+",
        "company_b": "BBB"
      }
    },
    {
      "column": "financial_risk_score",
      "values_by_company_id": {
        "company_a": "C",
        "company_b": "BB+"
      }
    },
    {
      "column": "blended_industry_risk_profile",
      "values_by_company_id": {
        "company_a": "A",
        "company_b": "A+"
      }
    },
    {
      "column": "competitive_positioning",
      "values_by_company_id": {
        "company_a": "B+",
        "company_b": "A+"
      }
    },
    {
      "column": "market_share",
      "values_by_company_id": {
        "company_a": "BB-",
        "company_b": "BBB+"
      }
    },
    {
      "column": "diversification",
      "values_by_company_id": {
        "company_a": "B+",
        "company_b": "A-"
      }
    },
    {
      "column": "operating_profitability",
      "values_by_company_id": {
        "company_a": "BB-",
        "company_b": "BB+"
      }
    },
    {
      "column": "sector_company_specific_factors_1",
      "values_by_company_id": {
        "company_a": "B-",
        "company_b": "BBB+"
      }
    },
    {
      "column": "leverage",
      "values_by_company_id": {
        "company_a": "CCC",
        "company_b": "BB+"
      }
    },
    {
      "column": "interest_cover",
      "values_by_company_id": {
        "company_a": "B-",
        "company_b": "A-"
      }
    },
    {
      "column": "cash_flow_cover",
      "values_by_company_id": {
        "company_a": "CCC",
        "company_b": "A-"
      }
    },
    {
      "column": "liquidity_adjustment_notches",
      "values_by_company_id": {
        "company_a": -2,
        "company_b": 1
      }
    },
    {
      "column": "credit_metrics",
      "values_by_company_id": {
        "company_a": [
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 18.491
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 21.532
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 4.862
          },
          {
            "locked": true,
            "year_label": "2018",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 36.8
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": null
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2025E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 27.329
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 4.862
          }
        ],
        "company_b": [
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "liquidity",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_debt_ebitda",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ebitda_interest_cover",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_ffo_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_focf_debt",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2019",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 1
          },
          {
            "locked": true,
            "year_label": "2020",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2021",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2022",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 2
          },
          {
            "locked": true,
            "year_label": "2023",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2024",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2025",
            "is_estimate": false,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2026E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2027E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          },
          {
            "locked": true,
            "year_label": "2028E",
            "is_estimate": true,
            "metric_name": "scope_adjusted_loan_value",
            "metric_value": 3
          }
        ]
      }
    }
  ],
  "request_uid": "f61034f5-2ddb-4460-88b1-ddc4e5318de4",
  "status": "OK"
}
```

### 9) snapshots list

- request:
```bash
curl -s "http://localhost:8000/v1/snapshots?country=Federal%20Republic%20of%20Germany"
```

- response:
```json
{
  "data": [
    {
      "snapshot_id": "a0965e29a04733781500a55428679883",
      "company_id": "company_a",
      "snapshot_created_at": "2026-03-01T06:21:45.134654Z",
      "snapshot_valid_from": "2026-02-25T23:54:55.274839Z",
      "company_scd_key": "936729c7acea324254f9cf87cb51c3ab",
      "company_name": "Company A",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "IFRS",
      "fiscal_year_end": "December",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "BBB",
      "industry_weight": "1.0",
      "segmentation_criteria": "EBITDA contribution",
      "rating_methodologies_applied": "General Corporate Rating Methodology",
      "document_version": 2,
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
      "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
      "business_risk_score": "B",
      "financial_risk_score": "CC",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "B+",
      "market_share": "B+",
      "diversification": "B+",
      "operating_profitability": "B",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 23
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 9
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    },
    {
      "snapshot_id": "71f44d93bca150d13615c25a69b32c6e",
      "company_id": "company_c",
      "snapshot_created_at": "2026-03-01T06:21:45.134654Z",
      "snapshot_valid_from": "2026-02-27T02:38:29.725072Z",
      "company_scd_key": "a8c31ad9afa00f9868e7301041b96738",
      "company_name": "Company C",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "US-GAAP",
      "fiscal_year_end": "November",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "A",
      "industry_weight": "1.0",
      "segmentation_criteria": "Revenue contribution",
      "rating_methodologies_applied": "Consumer Products Rating Methodology | General Corporate Rating Methodology",
      "document_version": 1,
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_C_1.xlsm",
      "source_modified_at_utc": "2026-02-27T02:38:29.725072Z",
      "business_risk_score": "A+",
      "financial_risk_score": "C",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "A+",
      "market_share": "BB-",
      "diversification": "A+",
      "operating_profitability": "BB-",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    }
  ],
  "request_uid": "c45497ea-bf88-4e7f-bed5-e2ca11a20cb1",
  "status": "OK"
}
```

### 10) snapshots latest

- request:
```bash
curl -s http://localhost:8000/v1/snapshots/latest
```

- response:
```json
{
  "data": [
    {
      "snapshot_id": "a0965e29a04733781500a55428679883",
      "company_id": "company_a",
      "snapshot_created_at": "2026-03-01T06:21:45.134654Z",
      "snapshot_valid_from": "2026-02-25T23:54:55.274839Z",
      "company_scd_key": "936729c7acea324254f9cf87cb51c3ab",
      "company_name": "Company A",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "IFRS",
      "fiscal_year_end": "December",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "BBB",
      "industry_weight": "1.0",
      "segmentation_criteria": "EBITDA contribution",
      "rating_methodologies_applied": "General Corporate Rating Methodology",
      "document_version": 2,
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
      "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
      "business_risk_score": "B",
      "financial_risk_score": "CC",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "B+",
      "market_share": "B+",
      "diversification": "B+",
      "operating_profitability": "B",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 23
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 22
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 29
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 9
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    },
    {
      "snapshot_id": "3522098e4dd616b69ef8f8a5412ba32b",
      "company_id": "company_b",
      "snapshot_created_at": "2026-03-01T07:16:50.341775Z",
      "snapshot_valid_from": "2026-03-01T07:16:29.318003Z",
      "company_scd_key": "14b30e889e0ed8624876d6683259f577",
      "company_name": "Company B",
      "country": "Swiss Confederation",
      "corporate_sector": "Automobiles & Parts",
      "reporting_currency": "CHF",
      "accounting_principles": "IFRS",
      "fiscal_year_end": "March",
      "industry_classification": "Automotive Suppliers | Automotive and Commercial Vehicle Manufacturers",
      "industry_risk_score": "BBB | BB",
      "industry_weight": "0.85 | 0.15",
      "segmentation_criteria": "EBITDA contribution",
      "rating_methodologies_applied": "Automotive and Commercial Vehicle Manufacturers Rating Methodology",
      "document_version": 4,
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_3.xlsm",
      "source_modified_at_utc": "2026-03-01T07:16:29.318003Z",
      "business_risk_score": "BBB-",
      "financial_risk_score": "BB",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "A+",
      "market_share": "BBB+",
      "diversification": "A-",
      "operating_profitability": "BB+",
      "sector_company_specific_factors_1": "BBB+",
      "leverage": "BB+",
      "interest_cover": "BBB+",
      "cash_flow_cover": "A-",
      "liquidity_adjustment_notches": 1,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 2
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 1
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2025",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        },
        {
          "locked": true,
          "year_label": "2028E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 3
        }
      ]
    },
    {
      "snapshot_id": "71f44d93bca150d13615c25a69b32c6e",
      "company_id": "company_c",
      "snapshot_created_at": "2026-03-01T06:21:45.134654Z",
      "snapshot_valid_from": "2026-02-27T02:38:29.725072Z",
      "company_scd_key": "a8c31ad9afa00f9868e7301041b96738",
      "company_name": "Company C",
      "country": "Federal Republic of Germany",
      "corporate_sector": "Personal & Household Goods",
      "reporting_currency": "EUR",
      "accounting_principles": "US-GAAP",
      "fiscal_year_end": "November",
      "industry_classification": "Consumer Products: Non-Discretionary",
      "industry_risk_score": "A",
      "industry_weight": "1.0",
      "segmentation_criteria": "Revenue contribution",
      "rating_methodologies_applied": "Consumer Products Rating Methodology | General Corporate Rating Methodology",
      "document_version": 1,
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_C_1.xlsm",
      "source_modified_at_utc": "2026-02-27T02:38:29.725072Z",
      "business_risk_score": "A+",
      "financial_risk_score": "C",
      "blended_industry_risk_profile": "A",
      "competitive_positioning": "A+",
      "market_share": "BB-",
      "diversification": "A+",
      "operating_profitability": "BB-",
      "sector_company_specific_factors_1": "B-",
      "leverage": "CCC",
      "interest_cover": "B-",
      "cash_flow_cover": "CCC",
      "liquidity_adjustment_notches": -2,
      "credit_metrics": [
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "liquidity",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_debt_ebitda",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ebitda_interest_cover",
          "metric_value": 18.491
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_ffo_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 21.532
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_focf_debt",
          "metric_value": 4.862
        },
        {
          "locked": true,
          "year_label": "2018",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2019",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2020",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2021",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2022",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 36.8
        },
        {
          "locked": true,
          "year_label": "2023",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": null
        },
        {
          "locked": true,
          "year_label": "2024",
          "is_estimate": false,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2025E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2026E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 27.329
        },
        {
          "locked": true,
          "year_label": "2027E",
          "is_estimate": true,
          "metric_name": "scope_adjusted_loan_value",
          "metric_value": 4.862
        }
      ]
    }
  ],
  "request_uid": "5b2d3f0c-d7fc-4747-8407-b476eb20beb6",
  "status": "OK"
}
```

### 11) uploads list

- request:
```bash
curl -s http://localhost:8000/v1/uploads
```

- response:
```json
{
  "data": [
    {
      "upload_id": "3dc9c679-204b-4010-bd51-0deca6a258a3",
      "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_3.xlsm",
      "source_filename": "corporates_B_3.xlsm",
      "source_modified_at_utc": "2026-03-01T07:16:29.318003Z",
      "file_size_bytes": 164114,
      "file_hash": "f3f9ef32038265f584cf9c080129c8f76b4cbd788bc1c9f03a5c9de4a72e4a34",
      "record_hash": "b1288b75a197c36d26fe651d6e7c5f5e9b75aa21ea2b95901ca7309c2e770911",
      "document_version": 4,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-03-01T07:16:40.556885Z"
    },
    {
      "upload_id": "a8ff5408-17af-4643-8b56-cd0d09fed0ba",
      "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-03-01T07:15:04.672667Z",
      "file_size_bytes": 164110,
      "file_hash": "f912994c1017a7df7cca88ed3bd735d48bc971a078d07396e6ac186fd8dc1b9a",
      "status": "validation_failed",
      "warning_count": 0,
      "error_count": 1,
      "error_message": "Business-rule validation failed for corporates_B_2.xlsm: industry_weight_sum: 1 violation(s)",
      "ingested_at": "2026-03-01T07:16:40.465208Z"
    },
    {
      "upload_id": "4cc6f38e-ea7c-43ad-9088-ce5801b4dd14",
      "run_id": "47eb4a46-9577-4b55-885d-aeaba3e6e77b",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-03-01T07:13:07.226959Z",
      "file_size_bytes": 164114,
      "file_hash": "11a5f928eb203498836b0a5a90961c2d725d8f3c82cc1886f86c28a88e027e68",
      "status": "validation_failed",
      "warning_count": 0,
      "error_count": 1,
      "error_message": "Validation failed for corporates_B_2.xlsm: [{'type': 'float_type', 'loc': ('credit_metrics', 0, 'values', 9, 'value'), 'msg': 'Input should be a valid number', 'input': 'A', 'url': 'https://errors.pydantic.dev/2.12/v/float_type'}]",
      "ingested_at": "2026-03-01T07:13:18.892935Z"
    },
    {
      "upload_id": "4a2abb58-b570-432e-971e-37c0f9138948",
      "run_id": "0b13f5bf-4416-4f9e-ad8f-305b7c8015b6",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-03-01T07:05:52.821222Z",
      "file_size_bytes": 164121,
      "file_hash": "58bcc0420de916c4950e4f380bd53a397586808cb9abb4a28add8ecce2b357ad",
      "status": "validation_failed",
      "warning_count": 0,
      "error_count": 1,
      "error_message": "Validation failed for corporates_B_2.xlsm: [{'type': 'float_type', 'loc': ('credit_metrics', 0, 'values', 9, 'value'), 'msg': 'Input should be a valid number', 'input': 'A', 'url': 'https://errors.pydantic.dev/2.12/v/float_type'}]",
      "ingested_at": "2026-03-01T07:06:06.820258Z"
    },
    {
      "upload_id": "5b061dfe-e5bb-4ec3-a0fc-6fd87f6c093b",
      "run_id": "890d84ed-4e27-49d0-b011-503c81b40f85",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-03-01T06:24:04.994117Z",
      "file_size_bytes": 164115,
      "file_hash": "6bc0e4ccc05647e60a66011848912a527b8cfa1721b9f2baf02514a289078001",
      "record_hash": "a9d7338ef18f0be16c419c4421e9939aeb7fbbd4f953a9fc643dbefc22272901",
      "document_version": 3,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-03-01T06:24:12.315787Z"
    },
    {
      "upload_id": "23e51ccc-83dd-4e3e-9f4a-f35da7126417",
      "run_id": "4784fc9b-df89-4b49-b226-4c516e138ceb",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-02-28T10:32:36.570924Z",
      "file_size_bytes": 164110,
      "file_hash": "8daf047f4d784b33789f878e357b6030d74545ac32f3c728b5a3cfa09a6ba22d",
      "record_hash": "1acf71a07c9977ae5d291324c4363a875b2b60d51bafcb96a4dd3e30ecec660c",
      "document_version": 2,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-03-01T06:21:32.897411Z"
    },
    {
      "upload_id": "92d20b55-c442-4bf7-b05a-8c219f99c822",
      "run_id": "4784fc9b-df89-4b49-b226-4c516e138ceb",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_C_1.xlsm",
      "source_filename": "corporates_C_1.xlsm",
      "source_modified_at_utc": "2026-02-27T02:38:29.725072Z",
      "file_size_bytes": 166978,
      "file_hash": "7fedcf7d1010eba1b50c898684963f95e30b9beeb77a37fc12f040c47dbbc591",
      "record_hash": "cf3438f1af58dbbcbf1d5d4cbd265aafaa4b78bc76f91cccf30003dcd8288a0e",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-03-01T06:21:32.800268Z"
    },
    {
      "upload_id": "f76ce52a-383f-49b3-be73-3e20584d2779",
      "run_id": "4784fc9b-df89-4b49-b226-4c516e138ceb",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
      "source_filename": "corporates_A_2.xlsm",
      "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
      "file_size_bytes": 164726,
      "file_hash": "0a5161e34e54a58320384ac130bd2119d8dca194f4cc0c37b8b55029fcb49102",
      "record_hash": "76bd249e4b526de24ed2e91c1055dc4cfaeefc458b744f4e0d62aac89b0e44a7",
      "document_version": 2,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-03-01T06:21:32.671288Z"
    },
    {
      "upload_id": "54e832d0-1311-4425-8605-d9745877c6ab",
      "run_id": "4784fc9b-df89-4b49-b226-4c516e138ceb",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_1.xlsm",
      "source_filename": "corporates_B_1.xlsm",
      "source_modified_at_utc": "2026-02-24T09:17:38.844634Z",
      "file_size_bytes": 146884,
      "file_hash": "ef043cca3abaf3922ed34b3c247f58bea68c13160d514dfcf5c2b503997ffef6",
      "record_hash": "9bc603e18cb9df08b0ecc8edf7a39f7b61b895df5de3e2bdc16b021ba44541b4",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-03-01T06:21:32.563805Z"
    },
    {
      "upload_id": "a944d595-847f-4945-9f0e-05544d7c08dd",
      "run_id": "4784fc9b-df89-4b49-b226-4c516e138ceb",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_1.xlsm",
      "source_filename": "corporates_A_1.xlsm",
      "source_modified_at_utc": "2026-02-24T09:17:38.844473Z",
      "file_size_bytes": 146963,
      "file_hash": "04bf22f57e2b75c4701c429d2ab988ed1d2bf86f29b5944b3d87185c2c7ee09b",
      "record_hash": "8abc17007a062ff231ed61cb36da853950a9200f4441d8e7a73e7369136e01ea",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-03-01T06:21:32.434276Z"
    },
    {
      "upload_id": "bfe43856-908c-4c2d-a7da-4b7b2f55c5fd",
      "run_id": "e271dd01-6d41-413d-8610-cfd9adbe3196",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-02-28T10:32:36.570924Z",
      "file_size_bytes": 164110,
      "file_hash": "8daf047f4d784b33789f878e357b6030d74545ac32f3c728b5a3cfa09a6ba22d",
      "record_hash": "1acf71a07c9977ae5d291324c4363a875b2b60d51bafcb96a4dd3e30ecec660c",
      "document_version": 4,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T10:32:51.981339Z"
    },
    {
      "upload_id": "685ac8fa-a5fb-4557-9ec3-63afdead181a",
      "run_id": "f0f1e763-0539-47b8-8d50-25c19fcd555f",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-02-28T10:03:21.691201Z",
      "file_size_bytes": 164115,
      "file_hash": "407f4104db45ca2f021e519036ee6e8470534db04c103916f2362adca190d538",
      "record_hash": "a9d7338ef18f0be16c419c4421e9939aeb7fbbd4f953a9fc643dbefc22272901",
      "document_version": 3,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T10:03:29.998516Z"
    },
    {
      "upload_id": "9d351661-527b-4302-a144-fb5c25a1a9a7",
      "run_id": "408d0560-7e73-4350-a16d-b66e58b72f3d",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-02-28T07:24:26.192238Z",
      "file_size_bytes": 164116,
      "file_hash": "05d32a68d21706877fdb71b2356a6a4158307aaa56163937ed9641ecfe39832a",
      "record_hash": "015753d00b8ca636e9803edd67f07436ec7333c86282b4d80654f91174fbda35",
      "document_version": 2,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T09:58:16.319558Z"
    },
    {
      "upload_id": "eb1df46d-da0e-4d8b-9331-be16834dd844",
      "run_id": "408d0560-7e73-4350-a16d-b66e58b72f3d",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_C_1.xlsm",
      "source_filename": "corporates_C_1.xlsm",
      "source_modified_at_utc": "2026-02-27T02:38:29.725072Z",
      "file_size_bytes": 166978,
      "file_hash": "7fedcf7d1010eba1b50c898684963f95e30b9beeb77a37fc12f040c47dbbc591",
      "record_hash": "cf3438f1af58dbbcbf1d5d4cbd265aafaa4b78bc76f91cccf30003dcd8288a0e",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T09:58:16.224422Z"
    },
    {
      "upload_id": "71d632a8-cc5f-499e-b913-157d36cedc0b",
      "run_id": "408d0560-7e73-4350-a16d-b66e58b72f3d",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
      "source_filename": "corporates_A_2.xlsm",
      "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
      "file_size_bytes": 164726,
      "file_hash": "0a5161e34e54a58320384ac130bd2119d8dca194f4cc0c37b8b55029fcb49102",
      "record_hash": "76bd249e4b526de24ed2e91c1055dc4cfaeefc458b744f4e0d62aac89b0e44a7",
      "document_version": 2,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T09:58:16.107443Z"
    },
    {
      "upload_id": "008f6fa6-7f93-41be-ba33-fe5b65def14a",
      "run_id": "408d0560-7e73-4350-a16d-b66e58b72f3d",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_1.xlsm",
      "source_filename": "corporates_B_1.xlsm",
      "source_modified_at_utc": "2026-02-24T09:17:38.844634Z",
      "file_size_bytes": 146884,
      "file_hash": "ef043cca3abaf3922ed34b3c247f58bea68c13160d514dfcf5c2b503997ffef6",
      "record_hash": "9bc603e18cb9df08b0ecc8edf7a39f7b61b895df5de3e2bdc16b021ba44541b4",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T09:58:16.009741Z"
    },
    {
      "upload_id": "30183710-5086-45e1-b52a-34517a12e68c",
      "run_id": "408d0560-7e73-4350-a16d-b66e58b72f3d",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_1.xlsm",
      "source_filename": "corporates_A_1.xlsm",
      "source_modified_at_utc": "2026-02-24T09:17:38.844473Z",
      "file_size_bytes": 146963,
      "file_hash": "04bf22f57e2b75c4701c429d2ab988ed1d2bf86f29b5944b3d87185c2c7ee09b",
      "record_hash": "8abc17007a062ff231ed61cb36da853950a9200f4441d8e7a73e7369136e01ea",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T09:58:15.910641Z"
    },
    {
      "upload_id": "91ab34e0-160b-4602-adec-e41678e156e9",
      "run_id": "8b3fe7c0-f651-42b2-a36c-1e4e4fa0b4d2",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-02-28T07:24:26.192238Z",
      "file_size_bytes": 164116,
      "file_hash": "05d32a68d21706877fdb71b2356a6a4158307aaa56163937ed9641ecfe39832a",
      "record_hash": "015753d00b8ca636e9803edd67f07436ec7333c86282b4d80654f91174fbda35",
      "document_version": 3,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-28T07:24:56.596087Z"
    },
    {
      "upload_id": "740f69ab-ae97-474b-800a-a0cb0d41969c",
      "run_id": "5f2be8fc-7058-4e1b-974d-acd833edcad7",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_C_1.xlsm",
      "source_filename": "corporates_C_1.xlsm",
      "source_modified_at_utc": "2026-02-27T02:38:29.725072Z",
      "file_size_bytes": 166978,
      "file_hash": "7fedcf7d1010eba1b50c898684963f95e30b9beeb77a37fc12f040c47dbbc591",
      "record_hash": "cf3438f1af58dbbcbf1d5d4cbd265aafaa4b78bc76f91cccf30003dcd8288a0e",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-27T12:05:59.960158Z"
    },
    {
      "upload_id": "33d995c8-b058-4a66-93ac-9cba790bc184",
      "run_id": "5f2be8fc-7058-4e1b-974d-acd833edcad7",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_2.xlsm",
      "source_filename": "corporates_A_2.xlsm",
      "source_modified_at_utc": "2026-02-25T23:54:55.274839Z",
      "file_size_bytes": 164726,
      "file_hash": "0a5161e34e54a58320384ac130bd2119d8dca194f4cc0c37b8b55029fcb49102",
      "record_hash": "76bd249e4b526de24ed2e91c1055dc4cfaeefc458b744f4e0d62aac89b0e44a7",
      "document_version": 2,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-27T12:05:59.861031Z"
    },
    {
      "upload_id": "b69bc207-c92b-4698-bc10-df954caae6a2",
      "run_id": "5f2be8fc-7058-4e1b-974d-acd833edcad7",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_2.xlsm",
      "source_filename": "corporates_B_2.xlsm",
      "source_modified_at_utc": "2026-02-25T22:37:26.360512Z",
      "file_size_bytes": 164785,
      "file_hash": "22d0e05dffaf98e4a3087a5b8bdafa309afd58b1901809bad5f99be069c0fa7f",
      "record_hash": "810d8e1e1ab0c68489f80da65d55f8811c77219ebb684b9470f69c0d4a093ed5",
      "document_version": 2,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-27T12:05:59.740384Z"
    },
    {
      "upload_id": "d64a7bc1-10f4-4a33-9785-345c97e83131",
      "run_id": "5f2be8fc-7058-4e1b-974d-acd833edcad7",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_B_1.xlsm",
      "source_filename": "corporates_B_1.xlsm",
      "source_modified_at_utc": "2026-02-24T09:17:38.844634Z",
      "file_size_bytes": 146884,
      "file_hash": "ef043cca3abaf3922ed34b3c247f58bea68c13160d514dfcf5c2b503997ffef6",
      "record_hash": "9bc603e18cb9df08b0ecc8edf7a39f7b61b895df5de3e2bdc16b021ba44541b4",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-27T12:05:59.608025Z"
    },
    {
      "upload_id": "7e647c43-763d-4007-aaf3-90fa08ebdd65",
      "run_id": "5f2be8fc-7058-4e1b-974d-acd833edcad7",
      "pipeline_name": "extract_company_history",
      "source_file_path": "/opt/airflow/repo/data/corporates/corporates_A_1.xlsm",
      "source_filename": "corporates_A_1.xlsm",
      "source_modified_at_utc": "2026-02-24T09:17:38.844473Z",
      "file_size_bytes": 146963,
      "file_hash": "04bf22f57e2b75c4701c429d2ab988ed1d2bf86f29b5944b3d87185c2c7ee09b",
      "record_hash": "8abc17007a062ff231ed61cb36da853950a9200f4441d8e7a73e7369136e01ea",
      "document_version": 1,
      "status": "inserted",
      "warning_count": 0,
      "error_count": 0,
      "ingested_at": "2026-02-27T12:05:59.400248Z"
    }
  ],
  "request_uid": "18daa75b-5ed5-49da-a947-bca11bf52fa0",
  "status": "OK"
}
```

### 12) uploads stats

- request:
```bash
curl -s http://localhost:8000/v1/uploads/stats
```

- response:
```json
{
  "data": {
    "total_uploads": 23,
    "successful_uploads": 20,
    "failed_uploads": 3,
    "total_warnings": 0,
    "total_errors": 3,
    "avg_file_size_bytes": 160112.13043478262,
    "latest_upload_at": "2026-03-01T07:16:40.556885Z",
    "uploads_by_status": {
      "validation_failed": 3,
      "inserted": 20
    }
  },
  "request_uid": "82d26a1e-bca8-4e11-a082-dd20d0bc1cfb",
  "status": "OK"
}
```

## Data quality report example

From `obs.data_quality_rule_results`:

- Query:
```sql
select run_id, scope, rule_id, severity, status, violations, details, created_at
from obs.data_quality_rule_results
order by created_at desc
limit 5;
```

- Results :

```json
[
  {
    "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
    "scope": "file",
    "rule_id": "credit_metrics_year_value_logic",
    "severity": "error",
    "status": "pass",
    "violations": 0,
    "details": null,
    "created_at": "2026-03-01 07:16:40.561812 +00:00"
  },
  {
    "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
    "scope": "file",
    "rule_id": "credit_metrics_outlier_values",
    "severity": "warning",
    "status": "pass",
    "violations": 0,
    "details": null,
    "created_at": "2026-03-01 07:16:40.561812 +00:00"
  },
  {
    "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
    "scope": "file",
    "rule_id": "industry_weight_sum",
    "severity": "error",
    "status": "pass",
    "violations": 0,
    "details": null,
    "created_at": "2026-03-01 07:16:40.561812 +00:00"
  },
  {
    "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
    "scope": "file",
    "rule_id": "score_scale_allowed",
    "severity": "error",
    "status": "pass",
    "violations": 0,
    "details": null,
    "created_at": "2026-03-01 07:16:40.561812 +00:00"
  },
  {
    "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
    "scope": "file",
    "rule_id": "credit_metrics_outlier_values",
    "severity": "warning",
    "status": "pass",
    "violations": 0,
    "details": null,
    "created_at": "2026-03-01 07:16:40.470402 +00:00"
  }
]
```

## Pipeline run event example

Printed by extraction pipeline and stored in `obs.pipeline_runs`:

- Query:
```sql
select *
from obs.pipeline_runs
order by created_at desc
limit 5;
```

- Results :

```json
[
  {
    "run_id": "b6cf2d01-138e-4879-a9b9-b6de126c6f1d",
    "pipeline_name": "extract_company_history",
    "started_at": "2026-03-01 07:57:09.695103 +00:00",
    "ended_at": "2026-03-01 07:57:09.864823 +00:00",
    "status": "success",
    "duration_seconds": 0.165653,
    "files_discovered": 1,
    "files_processed": 1,
    "rows_inserted": 0,
    "rows_skipped": 1,
    "warnings": 0,
    "errors": 0,
    "extraction_failures": 0,
    "validation_failures": 0,
    "load_failures": 0,
    "completeness_rate": 1,
    "validity_rate": 1,
    "created_at": "2026-03-01 07:57:09.754474 +00:00"
  },
  {
    "run_id": "7d484bc7-457f-470f-a6dc-e36dba9668e4",
    "pipeline_name": "extract_company_history",
    "started_at": "2026-03-01 07:16:40.338373 +00:00",
    "ended_at": "2026-03-01 07:16:40.575870 +00:00",
    "status": "failed",
    "duration_seconds": 0.234315,
    "files_discovered": 2,
    "files_processed": 2,
    "rows_inserted": 1,
    "rows_skipped": 1,
    "warnings": 0,
    "errors": 1,
    "extraction_failures": 0,
    "validation_failures": 1,
    "load_failures": 0,
    "completeness_rate": 0.5,
    "validity_rate": 0.5,
    "created_at": "2026-03-01 07:16:40.369823 +00:00"
  },
  {
    "run_id": "47eb4a46-9577-4b55-885d-aeaba3e6e77b",
    "pipeline_name": "extract_company_history",
    "started_at": "2026-03-01 07:13:18.774894 +00:00",
    "ended_at": "2026-03-01 07:13:18.909388 +00:00",
    "status": "failed",
    "duration_seconds": 0.130794,
    "files_discovered": 1,
    "files_processed": 1,
    "rows_inserted": 0,
    "rows_skipped": 1,
    "warnings": 0,
    "errors": 1,
    "extraction_failures": 0,
    "validation_failures": 1,
    "load_failures": 0,
    "completeness_rate": 0,
    "validity_rate": 0,
    "created_at": "2026-03-01 07:13:18.806990 +00:00"
  },
  {
    "run_id": "0b13f5bf-4416-4f9e-ad8f-305b7c8015b6",
    "pipeline_name": "extract_company_history",
    "started_at": "2026-03-01 07:06:06.665411 +00:00",
    "ended_at": "2026-03-01 07:06:06.849601 +00:00",
    "status": "failed",
    "duration_seconds": 0.177966,
    "files_discovered": 1,
    "files_processed": 1,
    "rows_inserted": 0,
    "rows_skipped": 1,
    "warnings": 0,
    "errors": 1,
    "extraction_failures": 0,
    "validation_failures": 1,
    "load_failures": 0,
    "completeness_rate": 0,
    "validity_rate": 0,
    "created_at": "2026-03-01 07:06:06.707258 +00:00"
  },
  {
    "run_id": "890d84ed-4e27-49d0-b011-503c81b40f85",
    "pipeline_name": "extract_company_history",
    "started_at": "2026-03-01 06:24:12.147547 +00:00",
    "ended_at": "2026-03-01 06:24:12.337337 +00:00",
    "status": "success",
    "duration_seconds": 0.186579,
    "files_discovered": 1,
    "files_processed": 1,
    "rows_inserted": 1,
    "rows_skipped": 0,
    "warnings": 0,
    "errors": 0,
    "extraction_failures": 0,
    "validation_failures": 0,
    "load_failures": 0,
    "completeness_rate": 1,
    "validity_rate": 1,
    "created_at": "2026-03-01 06:24:12.185462 +00:00"
  }
]
```
