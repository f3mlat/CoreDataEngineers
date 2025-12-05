from datetime import datetime
import pandas as pd

run_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

def add_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds ingestion metadata columns to a Pandas DataFrame.
    """
    df["ingestion_date"] = pd.Timestamp.utcnow().date()
    df["ingestion_timestamp"] = pd.Timestamp.utcnow()
    df["ingestion_run_id"] = run_datetime
    return df
