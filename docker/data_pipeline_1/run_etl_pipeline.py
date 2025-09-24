from sqlalchemy import create_engine
import pandas as pd
from extract import extract_data
from transform import transform_data
from load import load_to_dw
import os

postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_dw = os.getenv('POSTGRES_DW')
csv_url= os.getenv('CSV_URL')

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

run_etl(csv_url=csv_url, dw_engine_connect=dw_engine_connect)