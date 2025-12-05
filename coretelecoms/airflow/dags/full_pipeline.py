#from airflow import DAG
#from airflow.utils.task_group import TaskGroup
#from datetime import datetime
#
#with DAG(
#    'coretelecoms_full_pipeline',
#    schedule='0 3 * * *',
#    start_date=datetime(2025,11,18),
#    catchup=True
#) as dag:
#
#    from airflow.operators.trigger_dagrun import TriggerDagRunOperator
#
#    ingest = TriggerDagRunOperator(
#        task_id='trigger_ingestion',
#        trigger_dag_id='coretelecoms_ingestion'
#    )
#    transform = TriggerDagRunOperator(
#        task_id='trigger_dbt',
#        trigger_dag_id='coretelecoms_dbt_transform'
#    )
#
#    ingest >> transform