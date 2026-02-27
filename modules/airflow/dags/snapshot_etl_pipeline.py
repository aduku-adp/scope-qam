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
    description="Extract ratings, run snapshot dbt model, then snapshot dbt tests",
    start_date=datetime(2026, 2, 1),
    schedule="@daily",
    catchup=False,
    tags=["ratings", "etl", "dbt", "snapshot"],
) as dag:
    start = EmptyOperator(task_id="start")

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt run --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow --select snap_company"
        ),
        env=DB_ENV,
        append_env=True,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "cd /opt/airflow/repo/modules/dbt_qam "
            "&& dbt test --profiles-dir /opt/airflow/repo/modules/dbt_qam --target airflow --select snap_company"
        ),
        env=DB_ENV,
        append_env=True,
    )

    end = EmptyOperator(task_id="end")

    start >> dbt_run >> dbt_test >> end
