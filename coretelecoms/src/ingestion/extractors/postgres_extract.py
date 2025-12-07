import logging
import boto3
import pandas as pd
import psycopg2
from src.ingestion.extractors.metadata_append import add_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_credentials(path):
    ssm = boto3.client('ssm')
    response = ssm.get_parameters_by_path(
        Path=path
    )
    params = {}
    for param in response['Parameters']:
        key = param['Name'].split('/')[-1]  # Take last part of SSM path
        params[key] = param['Value']

    return params

def extract_db(query):
    ssm_path="/coretelecomms/database"
    conn_params = get_db_credentials(ssm_path)
    postgres_host = conn_params.get('db_host')
    postgres_port = conn_params.get('db_port')
    postgres_db = conn_params.get('db_name')
    postgres_user = conn_params.get('db_username')
    postgres_password = conn_params.get('db_password')

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=postgres_host,
        database=postgres_db,
        user=postgres_user,
        password=postgres_password,
        port=postgres_port
    )

    # Execute a sample query
    df = pd.read_sql(query, conn)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True)

    return add_metadata(df)