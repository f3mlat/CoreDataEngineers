import requests
import shutil
import os
from wikipedia_pageviews_pipeline.config.config import logger, TMP_DIR

def download_file(url: str, file_name: str) -> str:
    """
    Downloads the gun-zipped file from the given URL.
    """
    local_path = os.path.join(TMP_DIR, file_name)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        logger.info(f"Downloaded file: {local_path}")
        return local_path
    except requests.exceptions.RequestException as e:
        logger.error(f"Download failed: {e}")
        raise