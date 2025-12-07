# CoreTelecoms Data Platform

Modern Data Engineering with **Airflow, Amazon(IAM, S3, SSM), Google(IAM, GCS, BigQuery), dbt, and Docker.**

---

## 📌 Project Overview

The **CoreTelecoms Data Platform** is an end-to-end modern data engineering solution designed to ingest, transform, and deliver analytics-ready telecom datasets using a fully containerized, **metadata-driven** architecture.

The platform supports:

* Automated ingestion from different sources - Amazon S3, Google sheet, and PostgreSQL database to Google Cloud Storage
* Metadata-driven ingestion orchestration using Airflow
* Scalable transformations modeled with dbt (staging → intermediate → marts)
* Partitioned + clustered BigQuery optimized tables
* Local reproducibility using Docker Compose

---

## 🏗 Architecture Diagram

### **High-Level Architecture (ASCII)**

```
                ┌──────────────────────────┐
                │ Upstream Telecom Sources │
                └──────────────┬───────────┘
                               ▼
                  Google Cloud Storage (Datalake)
                               ▼
                ┌──────────────────────────┐
                │        Airflow DAGs      │
                │  - Ingestion Pipelines   │
                │  - dbt Run/Test/Docs     │
                └──────────────┬───────────┘
                               ▼
                ┌──────────────────────────┐
                │ BigQuery Data Warehouse  │
                │  • Raw Layer             │
                │  • Staging Layer (dbt)   │
                │  • Intermediate Layer    │
                │  • Datawarehouse         |
                |    (Analytics)           │
                └──────────────┬───────────┘
                               ▼
                ┌──────────────────────────┐
                │     BI / Analytics       │
                │  Looker / Tableau / DS   │
                └──────────────────────────┘
```

## 📁 Project Structure

```
├── airflow
│   ├── config
│   │   ├── airflow.cfg
│   │   └── metadata.yml                    # metadata of sources and their attributes
│   ├── dags
│   │   ├── bigquery_table_creation_dag.py
│   │   ├── dbt_transfrom_dag.py            # dbt run/test/docs orchestration
│   │   ├── full_pipeline.py
│   │   └── ingestion_dag.py                # Metadata-driven ingestion DAG
│   ├── dbt_transfrom_dag.py
│   ├── Dockerfile
│   └── requirements.txt
├── dbt
│   ├── dbt_project.yml
│   ├── Dockerfile
│   ├── macros
│   │   └── get_customer_age_group.sql
│   ├── models
│   │   ├── datawarehouse
│   │   │   └── customer_experience
│   │   │       ├── dim_agents.sql
│   │   │       ├── dim_customers.sql
│   │   │       └── fact_complaints.sql
│   │   ├── intermediate
│   │   │   ├── int_all_complaints.sql
│   │   │   └── int_customer_age_group.sql
│   │   └── staging
│   │       ├── schema.yml
│   │       ├── stg_agents.sql
│   │       ├── stg_call_center.sql
│   │       ├── stg_customers.sql
│   │       ├── stg_social_media.sql
│   │       └── stg_web_complaints.sql
│   ├── profiles.yml
│   └── tests
│       └── test_complaint_keys.sql
├── docker-compose.yml
├── .github
│   └── workflows
│       ├── cd.yml
│       └── ci.yml
├── .gitignore
├── README.md
├── src
│   ├── Dockerfile
│   ├── ingestion
│   │   ├── extractors
│   │   │   ├── google_sheets_extract.py
│   │   │   ├── metadata_append.py
│   │   │   ├── postgres_extract.py
│   │   │   └── s3_extract.py
│   │   └── requirements.txt
│   ├── load
│   │   └── load_to_gcs.py
│   ├── run_ingestion.py
│   └── utils
│       └── gcp_client.py
└── terraform
    ├── gcs.tf
    ├── iam.tf
    ├── main.tf
    ├── policy.tf
    ├── s3.tf
    └── variables.tf
```

---

## 🛠 Tools & Technologies

| Layer                           | Tool                                        |
| --------------------------------| --------------------------------------------|
| Orchestration                   | **Apache Airflow**                          |
| Data Warehouse                  | **Google BigQuery**                         |
| Storage                         | **Amazon S3**, **Google Cloud Storage**     |
| Transformations                 | **dbt-core + dbt-bigquery**                 |
| Runtime Environment             | **Docker + Docker Compose**                 |
| Metadata                        | YAML-based ingestion configs                |
| Infrastructure provisioning     | Terraform                                   |

---

## 🚀 Setup Instructions

### **1. Clone the Repository**

```bash
git clone https://github.com/f3mlat/CoreDataEngineers.git
cd coretelecoms
```

---

### **2. Create Service Account + Key**

```bash
gcloud iam service-accounts create airflow-sa \
  --display-name "Airflow Service Account"

gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member "serviceAccount:airflow-sa@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role "roles/bigquery.admin"

gcloud iam service-accounts keys create credentials/<credentials_file>.json \
  --iam-account airflow-sa@<PROJECT_ID>.iam.gserviceaccount.com
```

Place the key in:

```
/.google/creds/<credentials_file>.json
```

---

### **3. Start the Platform**

```bash
docker-compose up -d --build
```

Airflow UI → **[http://localhost:8080](http://localhost:8080)**

Credentials → `admin / admin`

---

### **4. Validate dbt Connection**

```bash
docker exec -it coretelecome-airflow-apiserver-1 bash
dbt debug --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt
```
---

## 🧩 Metadata-Driven Pipelines

Ingestion metadata lives in:

```
dags/metadata/pipelines.yml
```

Each dataset metadata defines:

* Type of source and storage - s3_csv, s3_json
* Bucket of source in cloud storage
* Key which details the folder_name/source_file_name
* Frequency of source - static, daily
* Destination path - GCS

This enables **zero-code ingestion changes** and **scalability**.

---

## 📊 dbt Modeling Layers

```
staging → intermediate → datawarehouse
```

### Includes:

* Source standardization
* Cleansing
* Feature enrichment
* Business-ready fact + dimension models
* Partitioned + clustered BigQuery tables

Example:

```sql
{{ config(
    materialized='table',
    partition_by={'field': 'ingestion_date', 'data_type': 'date'},
    cluster_by=['customer_state']
) }}
```

---

## 📦 Airflow DAGs

### **1. ingestion_dag.py**

* [Amazon S3, Google Sheet, PostgreSQL] → GCS raw ingestion
* Metadata-driven loader
* Automatic task generation

### **2. bigquery_table_creation_dag.py**

* Creates external table from parquet files
* Creates regular tables

---

### **3. dbt_transform_dag.py**

* Runs `dbt run`
* Runs `dbt test`
* Builds documentation

---

### **4. full_pipeline_dag.py**

* Runs the above 3 dags at a scheduled time

---

### Running the Pipeline

- **Trigger the DAG(s) Manually**
    Via Airflow UI:
    - Navigate to http://localhost:8080
    - Find the DAG - coretelecoms_full_pipeline
    - Toggle it ON
    - Click the "Trigger" button

---

## 🧪 Testing

```bash
dbt test
```

---

## 📘 Documentation

Generate and host dbt docs:

```bash
dbt docs generate
dbt docs serve
```

---

## 🛠 Troubleshooting

### ❌ BigQuery Authentication Error

Ensure correct profiles.yml:

```yaml
keyfile: /opt/airflow/.cred/<credentials_file>.json
```

---

## 👤 Author / Maintainer

Lateef – Data Engineer

---

## 🎉 Final Notes

This repository demonstrates a modern data engineering stack aligned with enterprise best practices.
It is fully reproducible, easily extendable, and ready for both learning and real-world deployment.

---