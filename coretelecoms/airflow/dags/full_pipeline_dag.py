from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

with DAG(
    'coretelecoms_full_pipeline',
    schedule='0 3 * * *',
    start_date=datetime(2025,11,18),
    catchup=True
) as dag:

    ingest = TriggerDagRunOperator(
        task_id="trigger_ingestion",
        trigger_dag_id="coretelecoms_source_ingestion",
        conf={
            "from_date": "2025-12-01",
            "to_date": "2025-12-07"
        }
    )

    create_bigquery_tables = TriggerDagRunOperator(
        task_id='trigger_bigquery',
        trigger_dag_id='coretelecoms_bigquery_tables'
    )

    transform = TriggerDagRunOperator(
        task_id='trigger_dbt',
        trigger_dag_id='coretelecoms_dbt_transform'
    )

    ingest >> create_bigquery_tables >> transform