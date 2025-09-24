#! \bin\bash

# Docker Automation Bash Script
# Author: Lateef Akinola
# Date: 2025-09-24
# Description: This script run docker containers that performs a simple ETL process: Extract, Transform, Load.

# Export the environment variables to be use in the docker containers
source ./export_var.sh
NETWORK_NAME=etlnetwork

# Stop and remove all containers connect to docker network
docker container rm $(docker stop $(docker ps -q -f "network=$NETWORK_NAME")) &> /dev/null

# Remove network
docker network rm $NETWORK_NAME &> /dev/null

# Create docker network that all the containers uses to communicate
docker network create $NETWORK_NAME &> /dev/null

# ETL process docker container build
docker build -t etlcontainer .

# PostgreSQL database docker container run
docker run -d -it --name postgresDB \
 -e POSTGRES_USER=postgres \
 -e POSTGRES_PASSWORD=postgres \
 -e POSTGRES_DB=cdeDW \
 --network=$NETWORK_NAME \
 postgres &> /dev/null

## PGAdmin to connect to postgreSQL
#docker run -d --name pgadmin \
# -e "PGADMIN_DEFAULT_EMAIL=admin@admin.com" \
# -e "PGADMIN_DEFAULT_PASSWORD=root" \
# -p 8080:80 \
# --network=$NETWORK_NAME \
# dpage/pgadmin4 &> /dev/null

CONTAINER_NAME=finance_etl
#Remove container
docker container rm -f $CONTAINER_NAME &> /dev/null

# ETL process docker container run
docker run -it --name $CONTAINER_NAME \
 -e POSTGRES_USER=$POSTGRES_USER \
 -e POSTGRES_USER=$POSTGRES_USER \
 -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
 -e POSTGRES_HOST=$POSTGRES_HOST \
 -e POSTGRES_PORT=$POSTGRES_PORT \
 -e POSTGRES_DW=$POSTGRES_DW \
 -e CSV_URL=$CSV_URL \
 --network=$NETWORK_NAME \
 etlcontainer