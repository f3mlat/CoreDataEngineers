FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./export_var.sh /app/export_var.sh
COPY ./extract.py /app/extract.py
COPY ./transform.py /app/transform.py
COPY ./load.py /app/load.py
COPY ./run_etl_pipeline.py /app/run_etl_pipeline.py


ENTRYPOINT ["python", "run_etl_pipeline.py"]