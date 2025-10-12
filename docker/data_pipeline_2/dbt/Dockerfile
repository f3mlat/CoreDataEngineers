FROM ghcr.io/dbt-labs/dbt-postgres:1.9.latest

WORKDIR /dbt

COPY . .

#RUN chmod +x run_dbt.sh

# Run ETL by default
#CMD ["/dbt/run_dbt.sh"]
CMD ["build"]