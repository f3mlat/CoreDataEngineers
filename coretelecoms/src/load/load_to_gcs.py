from google.cloud import storage
from google.oauth2 import service_account
import pyarrow as pa
import pyarrow.parquet as pq
from src.utils.gcp_client import get_gcs_client

def write_parquet_to_gcs(df, gcs_path):
    """
    Upload a pandas dataframe to google cloud storage as parquet.
    gcs_path format: gs://bucket-name/path/to/file.parquet
    """

    # parse gs://bucket/path
    if not gcs_path.startswith("gs://"):
        raise ValueError("GCS path must start with gs://")

    bucket_name, *blob_parts = gcs_path.replace("gs://", "").split("/")
    blob_name = "/".join(blob_parts)

    if not bucket_name or not blob_name:
        raise ValueError(f"Invalid GCS path: {gcs_path}")

    print(f"Preparing to upload to bucket={bucket_name}, blob={blob_name}")

    # convert dataframe to arrow Table
    table = pa.Table.from_pandas(df)

    # write to in-memory buffer
    buffer = pa.BufferOutputStream()
    pq.write_table(table, buffer)
    data = buffer.getvalue().to_pybytes()

    # upload to google cloud storage
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data, content_type="application/octet-stream")

    print(f"Uploaded parquet to: {gcs_path}")