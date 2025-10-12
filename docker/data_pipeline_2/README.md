## Dockerized ELT Pipeline
### 📌Overview

This project demonstrates a fully automated ELT pipeline using Docker.
The pipeline consists of three containers/services:

1. **Python (ETL)** → Extracts CSV data from a URL and loads it into Postgres.
2. **Postgres** → Staging database to hold raw and transformed data.
3. **DBT** → Transforms the staged data into a clean analytics model.

The pipeline is scheduled to run **daily at 12:00 a.m.** using a cron job.


## 🏗 Architecture
![Pipeline Architecture](diagrams/pipeline_architecture.png)


## 📂 Project Structure
```
.
├── dbt
│   ├── dbt_project.yml
│   ├── Dockerfile
│   ├── export_var.sh
│   ├── logs
│   │   └── dbt.log
│   ├── models
│   │   ├── analytics
│   │   │   ├── dim_finance_summary.sql
│   │   │   └── schema.yml
│   │   └── staging
│   │       ├── schema.yml
│   │       └── stg_finance.sql
│   └── profiles.yml
├── docker-compose.yaml
├── etl
│   ├── Dockerfile
│   ├── etl.py
│   ├── extract_data.py
│   ├── load_data.py
│   ├── requirements.txt
│   └── run_etl.sh
├── raw.csv
├── README.md
└── scripts
    ├── export_var.sh
    └── run_pipeline.sh
```

## ⚙️ Prerequisites
- Linux environment
- Bash shell
- Docker Docker & Docker Compose
- Python
- git
- PostgreSQL client (optional, for testing)


## 🚀 Running the Pipeline
### 1. Build & Start Containers
```shell
source scripts/run_pipeline.sh
```
This will:
- Starts Postgres container
- Starts and run the Python ETL container (extract + load)
- Starts and run DBT container (transform data)

### 2. Verify Data

You can connect to Postgres locally:

psql -h localhost -U user -d <database_name>

### 3. Schedule Daily Run

Edit crontab with crontab -e and add:

0 0 \* \* \* /home/l/etl-pipeline-docker/scripts/run_pipeline.sh >> /home/l/etl-pipeline-docker/logs/pipeline.log 2>&1

This ensures the pipeline runs every midnight.

### Dockerized ETL Lifecycle
1. **Extract (Python)** → download and clean data
2. **Load (Postgres)** → save to staging database
3. **Transform (dbt)** → create analytics-ready models
4. **Schedule (cron)** → run daily automatically


