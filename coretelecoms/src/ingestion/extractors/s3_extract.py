import pandas as pd
from ingestion.extractors.metadata_append import add_metadata
import boto3

def extract_csv(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj['Body'])

    # Clean column names
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]

    return add_metadata(df)

def extract_json(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_json(obj['Body'])

    # Clean column names
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]

    return add_metadata(df)