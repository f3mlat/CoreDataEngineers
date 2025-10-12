import os
from sqlalchemy import create_engine
from extract_data import extract_csv
from load_data import load


# --- Config (use env vars for flexibility) ---
CSV_URL = os.getenv("CSV_URL")

df = extract_csv(CSV_URL)
load(df)