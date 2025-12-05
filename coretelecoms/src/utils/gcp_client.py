from google.cloud import storage
import os

def get_gcs_client():

    credentials_file = "/opt/.google/creds/coretelecoms.json"

    if not os.path.exists(credentials_file):
        raise FileNotFoundError(f"Google credentials not found: {credentials_file}")

    return storage.Client.from_service_account_json(credentials_file)