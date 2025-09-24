import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower() for col in df.columns]
    return df