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
    dag_id="snapshot_etl_pipeline",
    description="Run snapshot dbt model and tests for snap_company",
    start_date=datetime(2026, 2, 1),
    schedule="@daily",
    catchup=False,
    tags=["ratings", "etl", "dbt", "snapshot"],
) as dag:
    start = EmptyOperator(task_id="start")

    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt run --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow --select snap_company"
        ),
        env=DB_ENV,
        append_env=True,
    )

    run_dbt_tests = BashOperator(
        task_id="run_dbt_tests",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt test --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow --select snap_company"
        ),
        env=DB_ENV,
        append_env=True,
    )

    end = EmptyOperator(task_id="end")

    start >> run_dbt_models >> run_dbt_tests >> end
