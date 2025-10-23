import sqlite3
import os
from wikipedia_pageviews_pipeline.config.config import COMPANIES, DB_PATH, logger

def parse_and_load(extracted_file: str, timestamp: str):
    """
    Parses the extracted file, filters for companies, aggregates views, and loads into SQLite.
    """

    ## Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pageviews (
            timestamp TEXT,
            page_title TEXT,
            views INTEGER,
            UNIQUE(timestamp, page_title)
        )
    ''')

    view_counts = {title: 0 for title in COMPANIES.values()}

    try:
        with open(extracted_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                domain, page_title, views_str = parts[:3]
                if domain.startswith('en') and page_title in view_counts:
                    view_counts[page_title] += int(views_str)

        for page_title, views in view_counts.items():
            if views > 0:
                cursor.execute('''
                    INSERT OR REPLACE INTO pageviews (timestamp, page_title, views)
                    VALUES (?, ?, ?)
                ''', (timestamp, page_title, views))

        conn.commit()
        logger.info(f"Data loaded for timestamp: {timestamp}")
    except Exception as e:
        logger.error(f"Load failed: {e}")
        raise
    finally:
        conn.close()
        # Clean up
        if os.path.exists(extracted_file):
            os.remove(extracted_file)
            logger.info(f"Cleaned up: {extracted_file}")