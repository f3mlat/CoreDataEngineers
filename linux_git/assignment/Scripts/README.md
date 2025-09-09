# Overview

Welcome to the Linus/Git assignment repository!
This assignment is to gets my hands dirty with the comcepts learnt in the Linux/Git class of the CDE 2.0 cohort class.
This repository contains Bash scripts to perform a simple ETL process, move JSON/CSV files, and import CSVs into PostgreSQL. It also contains SQL scripts to answer Ayoola's questions.

## Prerequisites
- Linux environment
- Bash shell
- curl
- psql (PostgreSQL client)
- git

## Files
See `Scripts/bash` and `Scripts/sql`.

## ETL Architecture

The etl architecture for the first question of the assignment is shown in the diagram below.
![ETL Architecture](docs\csv_etl_architecture.png)

## ETL

1. Export URL:

export CSV_URL="https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2023-financial-year-provisional/Download-data/annual-enterprise-survey-2023-financial-year-provisional.csv"

Run with:

bash Scripts/bash/csv_etl.sh

* Downloads CSV -> raw/

* Transforms file -> Transformed/2023_year_finance.csv

* Copies transformed file -> Gold/

3. Check folders to confirm that file was loaded `assignment/raw`, `assignment/Transformed`, `assignment/Gold`.

## Schedule with cron

Add this line to crontab (`crontab -e`):

0 0 * * * /bin/bash Scripts/Bash/csv_etl.sh >> Scripts/Bash/csv_etl.log

## Move CSV and JSON files

Run with:
bash Scripts/bash/csv_json_move.sh

* Moves .csv and .json files -> json_and_CSV/

## Copy CSV files into PostgreSQL (posey)

1. Set database environment variables:

export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
Add password in the .pgpass for security

Run with:
bash Scripts/bash/csv_to_postgresql_load.sh

* Imports all CSVs in current folder to PostgreSQL tables named after each CSV.

## SQL queries

See `Scripts/sql/` for the SQL files that answer the requested queries.

* query_1.sql -> Orders where gloss_qty or poster_qty > 4000
* query_2.sql -> Orders where standard_qty = 0 AND (gloss_qty or poster_qty > 1000)
* query_3.sql -> Account names starting with C or W, contact contains "ana" but not "eana"
* query_4.sql -> Regions, sales reps, and accounts sorted alphabetically

Run them with:
psql -d posey -f Scripts/sql/query_1.sql
psql -d posey -f Scripts/sql/query_2.sql
psql -d posey -f Scripts/sql/query_3.sql
psql -d posey -f Scripts/sql/query_4_.sql

## 📂 Repository Structure
```
├── linux_git
│   └── assignment
│       ├── data
│       │   ├── accounts.csv
│       │   ├── orders.csv
│       │   ├── region.csv
│       │   ├── sales_reps.csv
│       │   └── web_events.csv
│       ├── Gold
│       │   └── 2023_year_finance.csv
│       ├── json_and_CSV
│       │   ├── customer.csv
│       │   ├── employees.csv
│       │   ├── package.json
│       │   ├── person.JSON
│       │   └── product.CSV
│       ├── raw
│       │   └── annual-enterprise-survey-2023-financial-year-provisional.csv
│       ├── Scripts
│       │   ├── Bash
│       │   │   ├── csv_etl.log
│       │   │   ├── csv_etl.sh
│       │   │   ├── csv_json_move.sh
│       │   │   └── csv_to_postgresql_load.sh
│       │   ├── README.md
│       │   └── SQL
│       │       ├── query_1.sql
│       │       ├── query_2.sql
│       │       ├── query_3.sql
│       │       └── query_4.sql
│       └── Transformed
│           └── 2023_year_finance.csv
└── README.md
```