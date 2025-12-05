from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

DBT_PROJECT_DIR = "/opt/airflow/dbt/coretelecoms_dbt"

with DAG(
    dag_id="coretelecoms_dbt_transform",
    schedule=None,
    start_date=datetime(2025, 11, 18),
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
        cd {DBT_PROJECT_DIR}
        dbt run --profiles-dir .
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        cd {DBT_PROJECT_DIR}
        dbt test --profiles-dir .
        """,
    )

    dbt_run >> dbt_test