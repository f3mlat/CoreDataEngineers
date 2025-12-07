from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml
from src.run_ingestion import ingest_source

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'coretelecoms_source_ingestion',
    description='DAG to ingest all sources based on metadata.yaml with date parameters',
    start_date=datetime(2025, 12, 4),
    catchup=False,
    default_args=default_args,
    tags=['coretelecoms', 'ingestion']
) as dag:

    # Load sources from metadata
    with open('/opt/airflow/config/metadata.yml') as f:
        metadata = yaml.safe_load(f)
    sources = metadata.get('sources', {})

    # Loop through all sources in metadata
    for source_name, config in sources.items():
        task = PythonOperator(
            task_id=f'ingest_{source_name}',
            python_callable=ingest_source,
            op_kwargs={
                'source_name': source_name,
                'config': config,
                # These can come from DAG run configuration
                'from_date': "{{ dag_run.conf.get('from_date', None) }}",
                'to_date': "{{ dag_run.conf.get('to_date', None) }}"
            }
        )