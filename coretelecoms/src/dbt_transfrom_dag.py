from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.task.trigger_rule import TriggerRule
from airflow.providers.smtp.operators.smtp import EmailOperator
import pandas as pd
from src.utils.gcp_client import get_gcs_client

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

EMAIL_RECIPIENTS = ["akinolal@gmail.com"]

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
    # Task 1: Load seeds from GCS
    # -------------------------------------------------------------------------
    def load_seed_from_gcs(bucket_name: str, source_path: str, target_csv_path: str):
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(source_path)
        blob.download_to_filename("/tmp/temp_seed.parquet")
        df = pd.read_parquet("/tmp/temp_seed.parquet")
        df.to_csv(target_csv_path, index=False)
        print(f"Seed file written to {target_csv_path}")

    load_seed_tasks = []
    for seed_name, gcs_path in SEED_FILES.items():
        csv_path = f"{DBT_PROJECT_DIR}/seeds/{seed_name}.csv"
        task = PythonOperator(
            task_id=f"load_seed_{seed_name}",
            python_callable=load_seed_from_gcs,
            op_kwargs={
                "bucket_name": SEED_BUCKET,
                "source_path": gcs_path,
                "target_csv_path": csv_path,
            },
        )
        load_seed_tasks.append(task)

    # -------------------------------------------------------------------------
    # Task 2: dbt Seed
    # -------------------------------------------------------------------------
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"""
        dbt seed --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}
        """,
        env={
            "DBT_PROFILES_DIR": DBT_PROFILES_DIR
        },
        append_env=True,
    )

    # -------------------------------------------------------------------------
    # Task 3: dbt Run
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
    # Task 4: dbt Test
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
    # Task 5: dbt Docs (optional)
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

    # -------------------------------------------------------------------------
    # Task 6: Success Notification via Email
    # -------------------------------------------------------------------------
    notify_success = EmailOperator(
        task_id="notify_success",
        to=EMAIL_RECIPIENTS,
        subject="dbt Transform Completed Successfully",
        html_content="""
        <h3>dbt Transform Completed Successfully!</h3>
        <ul>
            <li>DAG: {{ dag.dag_id }}</li>
            <li>Run: {{ dag_run.run_id }}</li>
        </ul>
        """,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    # -------------------------------------------------------------------------
    # TASK DEPENDENCIES
    # -------------------------------------------------------------------------
    for t in load_seed_tasks:
        t >> dbt_seed

    dbt_seed >> dbt_run >> dbt_test >> dbt_docs >> notify_success