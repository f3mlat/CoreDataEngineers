import os
import yaml
from datetime import datetime
from ingestion.extractors.s3_extract import extract_csv, extract_json
from ingestion.extractors.google_sheets_extract import extract_sheet
from ingestion.extractors.postgres_extract import extract_db

from load.load_to_gcs import write_parquet_to_gcs

def ingest_source(source_name: str, execution_date: str = None):
    """
    Ingest a single source based on metadata.yaml.
    Parameters:
        source_name (str): name of the source in metadata.yaml
        execution_date (str): YYYY-MM-DD string; defaults to today
    """
    if execution_date is None:
        execution_date = datetime.now().strftime("%Y-%m-%d")

    # Load source config
    with open("/home/dev/CoreDataEngineer/coretelecoms/airflow/config/metadata.yml" ) as f:  # adjust path if needed
        config = yaml.safe_load(f)['sources'][source_name]

    # Map source type to extractor function
    extractor_map = {
        's3_csv': lambda: extract_csv(config['bucket'], config['key'].format(ds=execution_date)),
        's3_json': lambda: extract_json(config['bucket'], config['key'].format(ds=execution_date)),
        'postgres': lambda: extract_db(config['query'].format(ds_nodash=execution_date.replace('-', '_'))),
        'google_sheet': lambda: extract_sheet(config['spreadsheet_id'], config['range'])
    }

    # extrcat data
    df = extractor_map[config['type']]()

    # generate gooogle cloud storage path
    # examplegs://[bucket-name]/[source-name]/data.parquet
    gcs_output = (
        f"{config['destination_path']}/"
        f"{source_name}/"
        f"{source_name}_{execution_date}.parquet"
    )

    # load data to gooogle cloud storage
    write_parquet_to_gcs(df, gcs_output)

    print(f"SUCCESS → {source_name} written to {gcs_output}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Standalone metadata-driven ingestion")
    parser.add_argument("source_name", type=str, help="Name of the source in metadata.yaml")
    parser.add_argument("--date", type=str, help="Execution date in YYYY-MM-DD format", default=None)

    args = parser.parse_args()

    ingest_source(source_name=args.source_name, execution_date=args.date)