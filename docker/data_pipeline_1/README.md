Welcome to the Docker ETL assignment repository!

## Assignment Overview
This assignment involves:

1. **Extract**: Download a CSV file from a URL.
2. **Transform**: Transform the data - change the column names from upercase to lower case.
3. **Load**: Loads the transformed data into the postgreSQL database.
4. **Dockerize**: Create docker containers for the above process - ETL, PostgresSQL, PGAdmin.
5. **Run**: Execute a bash script to create the docker containers.


#### Objective

The assignment is meant to **get hands dirty with the concepts learnt in the docker class**


## Prerequisites

- Linux environment
- Bash shell
- Docker
- Python
- git


## How to run pipeline
```shell
bash run_pipepline.sh
```
The above Bash script:

* Exports the environment variables
  
* Stop and remove all containers connect to docker network

* Remove network

* Create docker network that all the containers uses to communicate

* ETL process docker container build

* PostgreSQL database docker container run

* Remove container

* ETL process docker container run



## 📂 Repository Structure

```
docker
   └── data_pipeline_1
       ├── Dockerfile
       ├── export_var.sh
       ├── extract.py
       ├── load.py
       ├── README.md
       ├── requirements.txt
       ├── run_etl_pipeline.py
       ├── run_pipeline copy.sh
       ├── run_pipeline.sh
       └── transform.py
```
