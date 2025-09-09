#!/bin/bash

# ETL Bash Script
# Author: Lateef Akinola
# Date: 2025-09-04
# Description: This script performs a simple ETL process: Extract, Transform, Load.

# Environment variable for default working directory
WORKDIR="/home/dev/CoreDataEngineer/linux_git/assignment"

# Environment variable for directories
RAW_DIR="$WORKDIR/raw"
TRANSFORMED_DIR="$WORKDIR/Transformed"
GOLD_DIR="$WORKDIR/Gold"
OUT_FILE="2023_year_finance.csv"

# Create the directories if they do not exist
mkdir -p "$RAW_DIR" "$TRANSFORMED_DIR" "$GOLD_DIR"

# *******************************
# Extraction step
# *******************************

echo "Extracting..."

CSV_FILENAME=$(basename "$CSV_URL")
RAW_FILE="$RAW_DIR/$CSV_FILENAME"

curl -sSL "$CSV_URL" -o "$RAW_FILE"

# Confirm file downloaded
if [[ -f "$RAW_DIR/$CSV_FILENAME" ]]; then
    echo "File downloaded successfully to $RAW_DIR/$CSV_FILENAME"
else
    echo "ERROR: File download was not successful"
    exit 1
fi

# *******************************
# Transformation step
# *******************************

echo "Transformating..."

TRANSFORMED_FILE="$TRANSFORMED_DIR/$OUT_FILE"

# Rename column Variable_code to variable_code and select specific columns
# Assumption: CSV uses commas as delimiter

# Read the header (first line)
IFS=',' read -r -a headers < "$RAW_DIR/$CSV_FILENAME"

# Find column positions
for i in "${!headers[@]}"; do
    case "${headers[$i]}" in
        "Variable_code") headers[$i]="variable_code"; var=$((i+1)) ;;
        "variable_code") var=$((i+1)) ;;
        "year")          y=$((i+1)) ;;
        "Value")         v=$((i+1)) ;;
        "Units")         u=$((i+1)) ;;
    esac
done

# Write the new header after tranformation
echo "year,Value,Units,variable_code" > "$TRANSFORMED_FILE"

# Write the rest of the lines after the header
tail -n +2 "$RAW_DIR/$CSV_FILENAME" | while IFS=',' read -r -a fields; do
    echo "${fields[$((y-1))]},${fields[$((v-1))]},${fields[$((u-1))]},${fields[$((var-1))]}" >> "$TRANSFORMED_FILE"
done

# Confirm transformation
if [[ -f "$TRANSFORMED_FILE" ]]; then
    echo "Transformation successful. Transformed file saved to $TRANSFORMED_FILE"
else
    echo "ERROR: Transformation was not successful"
    exit 1
fi

# *******************************
# Load step
# *******************************

echo "Loading..."

cp "$TRANSFORMED_FILE" "$GOLD_DIR/"

# Confirm load
if [[ -f "$GOLD_DIR/$OUT_FILE" ]]; then
    echo "Load successful. Loaded file is now in $GOLD_DIR/"
else
    echo "ERROR: Load was not successful"
    exit 1
fi

echo "ETL Process Completed Successfully!"