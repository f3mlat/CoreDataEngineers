#!/usr/bin/env bash
# run_pipeline.sh
# Automates ETL → DBT sequence safely and logs progress

set -euo pipefail

# export needed environment variables
chmod +x scripts/export_var.sh
source scripts/export_var.sh

echo "Starting ETL & DBT Pipeline..."
echo "Timestamp: $(date)"
echo "----------------------------------------"

# Step 1: Run ETL container
echo "[1/3] Running ETL step..."
docker compose run --rm etl
ETL_EXIT_CODE=$?

if [ $ETL_EXIT_CODE -ne 0 ]; then
  echo "ETL step failed with exit code $ETL_EXIT_CODE."
  echo "Stopping pipeline."
  exit 1
else
  echo "ETL step completed successfully."
  echo
fi

# Step 2: Run DBT transformations
echo "[2/3] Running DBT transformations..."
docker compose run --rm dbt build
DBT_RUN_EXIT_CODE=$?

if [ $DBT_RUN_EXIT_CODE -ne 0 ]; then
  echo "DBT run failed with exit code $DBT_RUN_EXIT_CODE."
  exit 1
else
  echo "DBT transformations completed."
  echo
fi

# Step 3: Run DBT tests (optional)
echo "[3/3] Running DBT tests..."
docker compose run --rm dbt test
DBT_TEST_EXIT_CODE=$?

if [ $DBT_TEST_EXIT_CODE -ne 0 ]; then
  echo "Some DBT tests failed. Please check your models."
else
  echo "All DBT tests passed successfully."
  echo
fi

echo "Pipeline completed successfully at $(date)"
echo "----------------------------------------"