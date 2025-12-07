from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.task.trigger_rule import TriggerRule
# =============================================================================
# CONFIG
# =============================================================================
PROJECT_ID = "onyx-cosmos-480018-k1"
DBT_PROJECT_DIR = "/opt/airflow/dbt/"
DBT_PROFILES_DIR = "/opt/airflow/dbt"
SEED_BUCKET = "coretelecoms-capstone-datalake"
SEED_FILES = {
    "agents": "agents/agents.parquet",
}

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# =============================================================================
# DAG
# =============================================================================
with DAG(
    dag_id="coretelecoms_dbt_transform",
    default_args=default_args,
    description="Load seeds from GCS and run dbt transformations",
    start_date=datetime(2025, 12, 5),
    catchup=False,
    max_active_runs=1,
    tags=["dbt", "bigquery", "coretelecoms"],
) as dag:

    # -------------------------------------------------------------------------
    # Task 1: dbt Run
    # -------------------------------------------------------------------------
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
        dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}
        """,
        env={
            "DBT_PROFILES_DIR": DBT_PROFILES_DIR
        },
        append_env=True,
    )

    # -------------------------------------------------------------------------
    # Task 1: dbt Test
    # -------------------------------------------------------------------------
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        dbt test --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}
        """,
        env={
            "DBT_PROFILES_DIR": DBT_PROFILES_DIR
        },
        append_env=True,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    # -------------------------------------------------------------------------
    # Task 3: dbt Docs (optional)
    # -------------------------------------------------------------------------
    dbt_docs = BashOperator(
        task_id="dbt_docs",
        bash_command=f"""
        dbt docs generate --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}
        """,
        env={
            "DBT_PROFILES_DIR": DBT_PROFILES_DIR
        },
        append_env=True,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    dbt_run >> dbt_test >> dbt_docs