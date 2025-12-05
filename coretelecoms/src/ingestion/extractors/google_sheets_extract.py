from ingestion.extractors.metadata_append import add_metadata
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def extract_sheet(spreadsheet_id, worksheet_name):
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file("/opt/.google/creds/coretelecoms.json", scopes=scopes)

    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet(worksheet_name)

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Clean column names
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]

    return add_metadata(df)