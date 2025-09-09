#!/bin/bash

# CSV Files move
# Author: Lateef Akinola
# Date: 2025-09-04
# Description: This script moves all .csv and .json files from SOURCE_DIR (or current dir by default)
#              into TARGET_DIR/json_and_CSV


# Environment variable for default working directory
export WORKDIR="/home/dev/CoreDataEngineer/linux_git/assignment"

# source directory as first command line argument or defaults to current dir
SOURCE_DIR="${1:-.}"
# target directory json_and_CSV
TARGET_DIR="$WORKDIR/json_and_CSV"

# Create the target directory directory if it does not exist
mkdir -p "$TARGET_DIR"

# Array for files in source directory matching csv and json files (case-insensitive)
shopt -s nullglob
files=( "$SOURCE_DIR"/*.csv "$SOURCE_DIR"/*.CSV "$SOURCE_DIR"/*.json "$SOURCE_DIR"/*.JSON )

# Check if there are any csv or json file in source directory
echo ${#files[@]}
if [ "${#files[@]}" -eq 0 ]; then
  echo "No CSV or JSON files in $SOURCE_DIR."
  exit 2
fi

# Move files from source to target directory
echo "Moving ${#files[@]} files to $TARGET_DIR ..."
for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    # Move file and print a message about movement.
    mv -v "$file" "$TARGET_DIR/"
  fi
done

echo "Done."
