from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator

DB_ENV = {
    "PG_HOST": "postgres",
    "PG_PORT": "5432",
    "PG_USER": "postgres",
    "PG_PASSWORD": "postgres",
    "DB_NAME": "qam_db",
}


with DAG(
    dag_id="company_etl_pipeline",
    description="Extract company data, run dbt models + tests, run snapshot + tests",
    start_date=datetime(2026, 2, 1),
    schedule="@daily",
    catchup=False,
    tags=["ratings", "etl", "dbt"],
) as dag:
    start = EmptyOperator(task_id="start")

    extract_company_data = BashOperator(
        task_id="extract_company_data",
        bash_command=(
            "cd /opt/airflow/repo/modules/data-extraction "
            "&& python extract_company_history.py"
        ),
        env=DB_ENV,
        append_env=True,
    )

    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt run --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow"
        ),
        env=DB_ENV,
        append_env=True,
    )

    run_dbt_model_tests = BashOperator(
        task_id="run_dbt_model_tests",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt test --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow --exclude resource_type:snapshot"
        ),
        env=DB_ENV,
        append_env=True,
    )

    run_dbt_snapshot = BashOperator(
        task_id="run_dbt_snapshot",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt snapshot --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow --select snap_company"
        ),
        env=DB_ENV,
        append_env=True,
    )

    run_dbt_snapshot_tests = BashOperator(
        task_id="run_dbt_snapshot_tests",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt test --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow --select resource_type:snapshot"
        ),
        env=DB_ENV,
        append_env=True,
    )

    end = EmptyOperator(task_id="end")

    (
        start
        >> extract_company_data
        >> run_dbt_models
        >> run_dbt_model_tests
        >> run_dbt_snapshot
        >> run_dbt_snapshot_tests
        >> end
    )
