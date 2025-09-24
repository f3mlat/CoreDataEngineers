# Transform Python Script
# Author: Lateef Akinola
# Date: 2025-09-24
# Description: This script performs the Transform part of the ETL process.

import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower() for col in df.columns]
    return df