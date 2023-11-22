import os
from airflow import DAG
from airflow.providers.google.cloud.transfers.oracle_to_gcs import OracleToGCSOperator
from datetime import datetime


with DAG('OracleToBigqueryOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:
    t1 = OracleToGCSOperator(
        task_id='write-to-bucket',
        oracle_conn_id="oracle_con",
        gcp_conn_id="google_con",
        sql="SELECT * FROM nada",
        bucket="airflow-oracle-to-bq",
        filename="dump",
        export_format="csv"
    )
