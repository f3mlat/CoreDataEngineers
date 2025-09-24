# Load Python Script
# Author: Lateef Akinola
# Date: 2025-09-24
# Description: This script performs the Load part of the ETL process.

import pandas as pd

def load_to_dw(df: pd.DataFrame, dw_engine_connect) -> None:
    df.to_sql(name='enterprise-survey', con=dw_engine_connect, if_exists='replace', schema='public', index=False)