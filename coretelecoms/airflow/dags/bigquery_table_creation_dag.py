import os
os.environ["AIRFLOW_DISABLE_SDK_COMPAT"] = "1"

from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

PROJECT_ID = "onyx-cosmos-480018-k1"
DATASET = "coretelecoms_capstone_datawarehouse"
BUCKET = "coretelecoms-capstone-datalake"

TABLE_CONFIG = {
    "agents": {
        "path": "agents/*.parquet",
        "source_format": "PARQUET",
    },
    "call_center_logs": {
        "path": "call_center_logs/*.parquet",
        "source_format": "PARQUET",
    },
    "customers": {
        "path": "customers/*.parquet",
        "source_format": "PARQUET",
    },
    "social_media": {
        "path": "social_media/*.parquet",
        "source_format": "PARQUET",
    },
    "web_complaints": {
        "path": "web_complaints/*.parquet",
        "source_format": "PARQUET",
    },
}

default_args = {
    "start_date": datetime(2025, 12, 5),
}

with DAG(
    dag_id="coretelecoms_bigquery_tables",
    schedule=None,
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["bigquery", "external_tables", "coretelecoms"],
) as dag:

    for table_name, config in TABLE_CONFIG.items():

        # ------------------------------------------
        # 1. Create External Table
        # ------------------------------------------
        external_table_id = f"{table_name}_external"

        sql_external = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{PROJECT_ID}.{DATASET}.{external_table_id}`
        OPTIONS (
            format = '{config["source_format"]}',
            uris = ['gs://{BUCKET}/{config["path"]}']
        );
        """

        create_external = BigQueryExecuteQueryOperator(
            task_id=f"create_external_{table_name}",
            sql=sql_external,
            use_legacy_sql=False,
        )

        # ------------------------------------------
        # 2. Create Regular Table from External Table
        # ------------------------------------------
        regular_table_id = f"{table_name}"

        sql_regular = f"""
        CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.{regular_table_id}` AS
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{external_table_id}`;
        """

        create_regular = BigQueryExecuteQueryOperator(
            task_id=f"create_regular_{table_name}",
            sql=sql_regular,
            use_legacy_sql=False,
        )

        create_external >> create_regular