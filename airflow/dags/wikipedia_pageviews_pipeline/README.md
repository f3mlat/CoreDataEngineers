# Wikipedia Pageviews Pipeline

This project implements a Apache Airflow Directed Acyclic Graph (DAG) to process Wikipedia pageview data for five selected companies (Amazon, Apple, Facebook, Google, and Microsoft). The pipeline downloads hourly pageview dumps from Wikimedia, extracts the data, filters it for the specified companies, and loads it into a SQLite database for analysis. The goal is to identify the company with the highest pageviews for a given hour, orchestrated using Apache Airflow.

The solution is designed based on the provided project overview. It follows best practices such as idempotence, retries, failure alerts, and modular code organization for maintainability and scalability.

## Project Overview
### Objective
- Reinforce understanding of orchestration using Apache Airflow.
- Process Wikipedia pageview data to analyze trends for selected companies.
- Create a repeatable workflow that can be extended for other dates or companies.

### Data Source
- Hourly pageview dumps are sourced from [Wikimedia Dumps](https://dumps.wikimedia.org/other/pageviews/).
- Example file: `pageviews-20241010-160000.gz` (hour ending at 16:00 UTC on October 10, 2024).
- Each hourly dump is approximately 50 MB gzipped and 200-250 MB unzipped.

### Scope
- Focuses on data from October 2025 (e.g., October 01, 2025, 19:00 UTC).
- Filters pageviews for company pages: 'Amazon_(company)', 'Apple_Inc.', 'Facebook', 'Google', 'Microsoft'.
- Loads data into a local SQLite database for analysis.

## Project Folder Structure
```
wikipedia_pageviews_pipeline/
├── config                                              # Configuration files
│   └── config.py                                       # Constants and settings
├── README.md                                           # This file
├── requirements.txt                                    # Project dependencies
├── scripts                                             # Scripts
│   └── sql                                             # SQL scripts
│       └── company_with_highest_views.sql              # Highest compnay page view analysis script
├── utils                                               # Utility modules
│   ├── download.py                                     # Download functionality
│   └── load.py                                         # Parse and load functionality
└── wikipedia_pageviews_dag.py                          # Main DAG
```

## Setup Instructions
### Prerequisites
- **Python 3.8+**
- **Apache Airflow 2.10.1+**
- Internet connection to download Wikimedia dumps

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/wikipedia-pageviews-pipeline.git
   cd wikipedia-pageviews-pipeline
   ```

2. **Install Dependencies**
    - Install required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

3. **Initialize Airflow**
    - Set up an Airflow environment:
        ```bash
        airflow db init
        ```
    - Start the Airflow webserver and scheduler in separate terminals:
        ```bash
        airflow webserver --port 8080
        airflow scheduler
        ```
    - Access the Airflow UI at `http://localhost:8080`(default credentials: `admin/admin` if not changed).

4. **Configure DAG**
    - Copy the `wikipedia_pageviews_pipeline/` folder to your Airflow DAGs directory (e.g., `~/airflow/dags/`).
    - Ensure the `config/` and `utils/` directories are accessible (e.g., in the same folder for the dag in this case `wikipedia_pageviews_pipeline/` ).

## Usage
### Running the Pipeline

- **Trigger the DAG Manually**
    Via Airflow UI:
    - Navigate to http://localhost:8080
    - Find the DAG:  wikipedia_pageviews_pipeline
    - Toggle it ON
    - Click the "Trigger DAG" button

    Via CLI:
    ```bash
    airflow dags trigger wikipedia_pageviews_pipeline --conf '{"year": "2025", "month": "10", "day": "22", "hour": "16"}'
    ```

    -  `year`, `month`, `day`, `hour`: Specify the date and hour (24-hour format) for which to process data (e.g., October 22, 2025, 16:00 UTC).

- **Monitor Execution**
    - Check the Airflow UI for task status (e.g., `download_gz`, `extract_gz`, `parse_and_load`).
    - Logs are available in the UI or at `~/airflow/logs/`.

## Database
- Data is stored in `tmp/database/pageviews.db`(SQLite).
- Schema:
    -  `timestamp`(TEXT): Date and time of the hour (e.g., '2025-10-22 16:00:00').
    -  `page_title`(TEXT): Wikipedia page title (e.g., 'Google').
    -  `views`(INTEGER): Total pageviews for that hour.
    - Unique constraint on `(timestamp, page_title)` ensures idempotence.

## Analysis
After the pipeline runs successfully, query the database to find the company with the highest pageviews:
```sql
SELECT page_title, views
FROM pageviews
WHERE timestamp = '2025-10-22 16:00:00'
ORDER BY views DESC
LIMIT 1;
```
- Use any SQLite client (e.g. `sqlite3 tmp/database/pageviews.db`)  to execute the query.

## Example Output
For illustration (using daily data from October 01, 2024, as hourly dumps aren't directly summarizable):
|Company|Page Title|Views (Daily)|
|:------|:---------|:------------|
|Google|Google|1,110|
|Facebook|Facebook|922|
|Amazon|Amazon_(company)|320|
|Apple|Apple_Inc.|376|
|Microsoft|Microsoft|383|

- Hourly results will vary but follow a similar pattern.

## Development
### Modularity
 - **Config**: Edit `config/config.py` to update company lists or paths.
 - **Utils**: Extend `utils/download.py` and `utils/load.py `for additional functionality.
 - **DAG**: Modify `wikipedia_pageviews_dag.py` to add tasks or change workflow.

### Testing
 - Test utilities independently:
    ```python
    from utils.download import download_file
    # Example use with mock URL
    ```
 - Use Airflow's test mode or local Python scripts to validate logic.

### Scaling
 - For larger datasets, replace SQLite with PostgreSQL.
 - Instead of local `tmp/`, use cloud storage such as S3 for file storage
 - For multiple hours/days, employ parallel processing

## Notes
 - **Data Availability**: As of October 23, 2025, 09:00 CDT, hourly dumps may yet be available. Use historical data (e.g., 2024) for testing.
 - **Error Handling**: The pipeline includes  3 retries  with a  5-minute delay .
 - **Cleanup**: Temporary files are removed after processing.

## Acknowledgments
 - Data sourced from [Wikimedia Dumps](https://dumps.wikimedia.org/other/pageviews/).
 - Built with Apache Airflow and Python.