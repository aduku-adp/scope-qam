# Airflow Module

Airflow orchestration for the QAM pipeline using Docker Compose and Celery executor.


## Scope

This module contains:

- DAG definitions
- Airflow runtime config
- scheduler/webserver logs (mounted volume)

Main DAGs:

- [`company_etl_pipeline.py`](/modules/airflow/dags/company_etl_pipeline.py)
- [`snapshot_etl_pipeline.py`](/modules/airflow/dags/snapshot_etl_pipeline.py)

## DAGs

### `company_etl_pipeline` (`@daily`)


### DAG graph

![Airflow DAG graph](/images/airflow-dag.png)


Sequence:

1. `extract_company_data` (`python extract_company_history.py`)
2. `run_dbt_models`
3. `run_dbt_model_tests` (non-snapshot)
4. `run_dbt_snapshot` (`snap_company`)
5. `run_dbt_snapshot_tests`

### `snapshot_etl_pipeline` (`@daily`)

Sequence:

1. `run_dbt_models` (`dbt snapshot --select snap_company`)
2. `run_dbt_tests`

## Compose integration

`docker-compose.yaml` mounts this module as Airflow project dir:

- `./modules/airflow/dags -> /opt/airflow/dags`
- `./modules/airflow/logs -> /opt/airflow/logs`
- `./modules/airflow/config -> /opt/airflow/config`

Repository code is mounted into containers at:

- `/opt/airflow/repo`

That allows DAG bash tasks to call:

- `modules/data-extraction/extract_company_history.py`
- `modules/dbt_qam` commands

## Airflow image

Build script:

- [`tools/build-airflow.sh`](/tools/build-airflow.sh)

Dockerfile:

- [`tools/Dockerfile`](/tools/Dockerfile)

Build:

```bash
./tools/build-airflow.sh
```

## Run stack

From repository root:

```bash
docker compose up -d
```

Airflow UI:

- `http://localhost:8080`

Default credentials (from compose env):

- username: `airflow`
- password: `airflow`

## Common operational notes

- In Airflow containers, Postgres host must be `postgres` (service name), not `localhost`.
- dbt profile dir in DAG tasks is explicitly set to:
  - `/opt/airflow/repo/modules/dbt_qam`
- Example DAGs are disabled via:
  - `AIRFLOW__CORE__LOAD_EXAMPLES=false`

## Relevant files

- [`config/airflow.cfg`](/modules/airflow/config/airflow.cfg)
- [`dags/company_etl_pipeline.py`](/modules/airflow/dags/company_etl_pipeline.py)
- [`dags/snapshot_etl_pipeline.py`](/modules/airflow/dags/snapshot_etl_pipeline.py)
