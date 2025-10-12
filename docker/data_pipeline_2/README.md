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
- Docker & Docker Compose installed
- PostgreSQL client (optional, for testing)


## 🚀 Running the Pipeline
### 1. Build & Start Containers
source scripts/run_pipeline.sh

This will:
- Start Postgres container
- Start and run the Python ETL container (extract + load)
- Start and run DBT container (transform data)

### 2. Verify Data

You can connect to Postgres locally:

psql -h localhost -U user -d <database_name>

### 3. Schedule Daily Run

Edit crontab with crontab -e and add:

0 0 \* \* \* /home/l/etl-pipeline-docker/scripts/run_pipeline.sh >> /home/l/etl-pipeline-docker/logs/pipeline.log 2>&1

This ensures the pipeline runs every midnight.
