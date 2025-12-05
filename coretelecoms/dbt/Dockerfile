FROM ghcr.io/dbt-labs/dbt-bigquery:latest

# Set working directory inside the container
WORKDIR /dbt

# Copy your dbt project files into the container
COPY . .

# Install any additional Python dependencies for your dbt project
#RUN pip install -r requirements.txt

# You can then run dbt commands within the container
CMD ["build"]