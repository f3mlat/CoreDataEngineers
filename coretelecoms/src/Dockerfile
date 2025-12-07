FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first (caching)
COPY src/ingestion/requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source code
COPY src/. /app/src
COPY .creds/credentials /app/.creds/credentials
COPY .creds/coretelecoms.json /app/.creds/coretelecoms.json

# Make script executable
RUN chmod +x /app/src/run_ingestion.py

# Default command (can be overridden)
CMD ["python", "app/src/run_ingestion.py"]