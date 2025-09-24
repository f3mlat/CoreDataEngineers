# Extract Python Script
# Author: Lateef Akinola
# Date: 2025-09-24
# Description: This script performs the Extract part of the ETL process.

import pandas as pd

def extract_data(csv_url:str) ->pd.DataFrame:
    df = pd.read_csv(csv_url,sep=",")
    return df