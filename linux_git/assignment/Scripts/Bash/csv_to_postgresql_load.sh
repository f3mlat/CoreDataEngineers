#!/bin/bash

# CSV files copy into a database
# Author: Lateef Akinola
# Date: 2025-09-04
# Description: This script copies each of the CSV files into a PostgreSQL database

WORKDIR="/home/dev/CoreDataEngineer/linux_git/assignment"
CSV_DIR="$WORKDIR/data"
DB_NAME="posey"

for f in $CSV_DIR/*.csv; do
  table=$(basename "$f" .csv)
  echo "Importing $f into $table..."
  psql -h "$PGHOST" -U "$PGUSER" -d "$DB_NAME" -c "\copy $table FROM $f WITH CSV HEADER;"
done

# Check the exit status of the psql command
if [ $? -eq 0 ]; then
    echo "CSV data successfully imported into $table in $DB_NAME."
else
    echo "Error: CSV import failed."
fi
