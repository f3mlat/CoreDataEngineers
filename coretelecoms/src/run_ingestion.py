from datetime import datetime, timedelta
from src.ingestion.extractors.s3_extract import extract_csv, extract_json
from src.ingestion.extractors.google_sheets_extract import extract_sheet
from src.ingestion.extractors.postgres_extract import extract_db
from src.load.load_to_gcs import write_parquet_to_gcs

def ingest_source(source_name: str = None, config: str = None,from_date: str = None, to_date: str = None, **context):
    """
    Ingest data from various sources into google cloud storage as parquet.
    """
    import logging
    from airflow.models import TaskInstance

    ti: TaskInstance = context.get('ti')
    execution_date = context.get('execution_date', datetime.now())

    # Determine date range
    if not from_date:
        from_date = context.get('dag_run').conf.get('from_date', execution_date.strftime("%Y-%m-%d"))
    if not to_date:
        to_date = context.get('dag_run').conf.get('to_date', execution_date.strftime("%Y-%m-%d"))

    logging.info(f"Running ingestion for source {source_name} from {from_date} to {to_date}")

    # convert to datetime objects
    start_dt = datetime.strptime(from_date, "%Y-%m-%d")
    end_dt = datetime.strptime(to_date, "%Y-%m-%d")

    # function map for different extractors
    extractor_map = {
        's3_csv': lambda date: extract_csv(config['bucket'], config['key'].format(ds=date)),
        's3_json': lambda date: extract_json(config['bucket'], config['key'].format(ds=date)),
        'postgres': lambda date: extract_db(config['query'].format(ds_nodash=date.replace('-', '_'))),
        'google_sheet': lambda _: extract_sheet(config['spreadsheet_id'], config['range'])
    }

    if config['frequency'] == 'daily':
        # iterate over the date range for incremental loads
        current_dt = start_dt
        while current_dt <= end_dt:
            date_str = current_dt.strftime("%Y-%m-%d")
            logging.info(f"Extracting data for {source_name} on {date_str}")

            try:
                if config['type'] in ['s3_csv', 's3_json', 'postgres']:
                    df = extractor_map[config['type']](date_str)
                else:
                    df = extractor_map[config['type']](None)

                if df.empty:
                    logging.warning(f"No data extracted for {source_name} on {date_str}")
                else:
                    # Construct GCS path
                    gcs_output = (
                        f"{config['destination_path']}/"
                        f"{source_name}/"
                        f"{source_name}_{date_str}.parquet"
                    )
                    write_parquet_to_gcs(df, gcs_output)
                    logging.info(f"{source_name} data successfully written to {gcs_output}")

                    # Push to XCom
                    if ti:
                        ti.xcom_push(key=f"{source_name}_{date_str}_gcs_path", value=gcs_output)

            except Exception as e:
                logging.error(f"Error processing {source_name} for date {date_str}: {e}", exc_info=True)
                raise

            # Increment day
            current_dt += timedelta(days=1)
    else:
        try:
            df = extractor_map[config['type']](None)

            if df.empty:
                logging.warning(f"No data extracted for {source_name}")
            else:
                # Construct GCS path
                gcs_output = (
                    f"{config['destination_path']}/"
                    f"{source_name}/"
                    f"{source_name}.parquet"
                )
                write_parquet_to_gcs(df, gcs_output)

                logging.info(f"{source_name} data successfully written to {gcs_output}")
                # Push to XCom
                if ti:
                    ti.xcom_push(key=f"{source_name}_gcs_path", value=gcs_output)
        except Exception as e:
                logging.error(f"Error processing {source_name}: {e}", exc_info=True)
                raise