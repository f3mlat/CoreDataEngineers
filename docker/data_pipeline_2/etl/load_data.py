import os
import pandas as pd
from sqlalchemy import create_engine

# --- Config (use env vars for flexibility) ---
PG_HOST = os.getenv("POSTGRES_HOST",)
PG_PORT = os.getenv("POSTGRES_PORT")
PG_DB   = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASS = os.getenv("POSTGRES_PASSWORD")
TABLE   = os.getenv("DB_TABLE")

import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(dbname=f"postgres", user="postgres", password="postgres", host="postgres")
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'dwDB'")
exists = cursor.fetchone()
if not exists:
    cursor.execute(sql.SQL("CREATE DATABASE dwDB"))
    print("✅ Database 'posey' created.")

cursor.close()
conn.close()

def load(df: pd.DataFrame):
    """Load DataFrame into Postgres"""
    print("Loading into Postgres ...")
    conn_str = f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    engine = create_engine(conn_str)


    df.to_sql(TABLE, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into table '{TABLE}'.")