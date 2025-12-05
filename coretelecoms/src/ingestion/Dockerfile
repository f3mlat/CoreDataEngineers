FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first (caching)
COPY src/ingestion/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src

# Make script executable
RUN chmod +x /app/src/run_ingestion.py

# Default command (can be overridden)
CMD ["python", "app/src/run_ingestion.py"]