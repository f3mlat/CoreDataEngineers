# Use the official dbt-bigquery image
FROM ghcr.io/dbt-labs/dbt-bigquery:latest

# Set working directory
WORKDIR /dbt

# Create directories early (reduces layer churn)
RUN mkdir -p /dbt/.creds && \
    mkdir -p /dbt/coretelecoms_dbt

# Copy only project files first (faster caching)
COPY dbt/coretelecoms_dbt /dbt/coretelecoms_dbt
COPY dbt/profiles.yml /dbt/profiles.yml

# Copy credentials (kept separate to avoid cache busting)
COPY .creds/coretelecoms.json /dbt/.creds/coretelecoms.json

# Set environment variables so dbt finds the right profile
ENV DBT_PROFILES_DIR=/dbt \
    GOOGLE_APPLICATION_CREDENTIALS=/dbt/.creds/coretelecoms.json

# Optional: install extra dependencies
# COPY dbt/requirements.txt /dbt/requirements.txt
# RUN pip install -r /dbt/requirements.txt

# Default command – runs dbt build when container starts
CMD ["dbt", "build"]