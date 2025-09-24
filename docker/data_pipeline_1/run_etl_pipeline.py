# ETL pipeline Python Script
# Author: Lateef Akinola
# Date: 2025-09-24
# Description: This script runs the ETL process pipeline.

from sqlalchemy import create_engine
import pandas as pd
from extract import extract_data
from transform import transform_data
from load import load_to_dw
import os

# Get the needed parameter from the environment variable; this is to hide them from the script
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_dw = os.getenv('POSTGRES_DW')
csv_url= os.getenv('CSV_URL')

# Create engine to connect to PostgreSQL database
dw_engine_connect = create_engine(f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_dw}')

def run_etl(csv_url:str, dw_engine_connect):
    print('Extracting data...')
    df_extract = extract_data(csv_url)
    print('Extraction done\n')

    print('Carrying out transformation...')
    df_transform = transform_data(df_extract)
    print('Transformation done\n')

    print('Loading into the datawarehouse...')
    load_to_dw(df_transform, dw_engine_connect)
    print('Loading done')

# Run the pipeline
run_etl(csv_url=csv_url, dw_engine_connect=dw_engine_connect)