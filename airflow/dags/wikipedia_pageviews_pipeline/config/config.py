import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Companies - page titles in the dump
COMPANIES = {
    'Amazon': 'Amazon_(company)',
    'Apple': 'Apple_Inc.',
    'Facebook': 'Facebook',
    'Google': 'Google',
    'Microsoft': 'Microsoft'
}

# Period parameters - this can be changed
PERIOD_YEAR = '2025'
PERIOD_MONTH = '10'
PERIOD_DAY = '22'
PERIOD_HOUR = '16'  # Hour ending at 16:00

# Paths
DB_PATH = '/opt/airflow/dags/wikipedia_pageviews_pipeline/tmp/database/pageviews.db'
TMP_DIR = '/opt/airflow/dags/wikipedia_pageviews_pipeline/tmp'

# Wikimedia base URL
URL = 'https://dumps.wikimedia.org/other/pageviews/{year}/{year}-{month}/pageviews-{year}{month}{day}-{hour}0000.gz'