import os
from airflow import DAG
from airflow.providers.google.cloud.transfers.oracle_to_gcs import OracleToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime


with DAG('OracleToBigqueryOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:
    t1 = OracleToGCSOperator(
        task_id="write-to-bucket",
        oracle_conn_id="oracle_con",
        gcp_conn_id="google_con_without_json_key",
        impersonation_chain="knada-hyka@knada-gcp.iam.gserviceaccount.com",
        sql="SELECT * FROM nada",
        bucket="airflow-oracle-to-bq",
        filename="dump",
        export_format="csv"
    )

    t2 = GCSToBigQueryOperator(
        task_id="write-to-bq",
        bucket="airflow-oracle-to-bq",
        gcp_conn_id="google_con_without_json_key",
        destination_project_dataset_table="nada-dev-db2e.test.fra_oracle",
        impersonation_chain="knada-hyka@knada-gcp.iam.gserviceaccount.com",
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
        source_objects="dump",
        source_format="csv"
    )

    t1 >> t2
