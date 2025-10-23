from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.utils.email import send_email
from wikipedia_pageviews_pipeline.config.config import URL, PERIOD_YEAR, PERIOD_MONTH, PERIOD_DAY, PERIOD_HOUR, TMP_DIR
from wikipedia_pageviews_pipeline.utils.download import download_file
from wikipedia_pageviews_pipeline.utils.load import parse_and_load

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 22),
    ##'email_on_failure': True,
    ##'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    ##'on_failure_callback': lambda context: send_email(
    ##    to='your.email@example.com',
    ##    subject='Airflow Alert: Task Failed',
    ##    html_content=f"Task {context['task_instance'].task_id} failed."
    ##),
}

with DAG(
    dag_id='wikipedia_pageviews_pipeline',
    description='DAG for processing Wikipedia pageviews for selected companies',
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['data_engineering', 'wikipedia', 'pageviews'],
    params={
        'year': PERIOD_YEAR,
        'month': PERIOD_MONTH,
        'day': PERIOD_DAY,
        'hour': PERIOD_HOUR,
    }
):

    def get_download_params(**kwargs):
        params = kwargs['params']
        year = params['year']
        month = params['month']
        day = params['day']
        hour = params['hour']
        file_name = f'pageviews-{year}{month}{day}-{hour}0000.gz'
        url = URL.format(year=year, month=month, day=day, hour=hour)
        downloaded_file = download_file(url, file_name)
        kwargs['ti'].xcom_push(key='file_name', value=downloaded_file)
        kwargs['ti'].xcom_push(key='timestamp', value=f'{year}-{month}-{day} {hour}:00:00')

    def get_load_params(**kwargs):
        extracted_file = f"{kwargs['ti'].xcom_pull(task_ids='download_gz', key='file_name')}".replace('.gz', '')
        timestamp = kwargs['ti'].xcom_pull(task_ids='download_gz', key='timestamp')
        parse_and_load(extracted_file, timestamp)

    download_task = PythonOperator(
        task_id='download_gz',
        python_callable=get_download_params
    )

    extract_task = BashOperator(
        task_id='extract_gz',
        bash_command="gunzip -f {{ ti.xcom_pull(task_ids='download_gz', key='file_name') }}"
    )

    load_task = PythonOperator(
        task_id='parse_and_load',
        python_callable=get_load_params
    )

    download_task >> extract_task >> load_task