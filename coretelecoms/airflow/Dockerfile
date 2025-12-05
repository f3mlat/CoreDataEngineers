# ==================== STAGE 1: Base Airflow ====================
FROM apache/airflow:3.1.3-python3.11

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        git \
        curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install Python deps
COPY airflow/requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copy DAGs, source code, and DBT project
COPY airflow/dags /opt/airflow/dags
COPY src /opt/airflow/src
COPY dbt /opt/airflow/dbt

# Set Python path
ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"

# Expose Airflow webserver port
EXPOSE 8080

# Default command overridden by docker-compose
CMD ["airflow", "standalone"]