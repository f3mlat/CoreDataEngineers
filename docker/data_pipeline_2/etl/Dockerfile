FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL script
COPY run_etl.sh .
COPY extract_data.py .
COPY load_data.py .
COPY etl.py .

RUN chmod +x run_etl.sh

# Run ETL by default
CMD ["/app/run_etl.sh"]