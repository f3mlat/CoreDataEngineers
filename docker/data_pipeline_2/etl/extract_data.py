import requests
import pandas as pd

def extract_csv(url: str) -> pd.DataFrame:
    """Download CSV and return as DataFrame"""
    print(f"Downloading CSV from {url} ...")
    response = requests.get(url)
    response.raise_for_status()

    # Save locally (optional)
    with open("raw.csv", "wb") as f:
        f.write(response.content)

    df = pd.read_csv("raw.csv")
    print(f"Extracted {len(df)} rows.")
    return df