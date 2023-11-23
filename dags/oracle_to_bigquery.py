import os
from airflow import DAG
from airflow.providers.google.cloud.transfers.oracle_to_gcs import OracleToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.gcs_delete_operator import GoogleCloudStorageDeleteOperator
from datetime import datetime


def oracle_to_bigquery(
    oracle_con_id: str,
    oracle_table: str,
    gcp_con_id: str,
    bigquery_dest_uri: str
):
    oracle_to_bucket = OracleToGCSOperator(
        task_id="oracle-to-bucket",
        oracle_conn_id=oracle_con_id,
        gcp_conn_id=gcp_con_id,
        impersonation_chain=f"{os.getenv('TEAM')}@knada-gcp.iam.gserviceaccount.com",
        sql=f"SELECT * FROM {oracle_table}",
        bucket=os.getenv("AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER").removeprefix("gs://"),
        filename=oracle_table,
        export_format="csv"
    )

    bucket_to_bq = GCSToBigQueryOperator(
        task_id="bucket-to-bq",
        bucket=os.getenv("AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER").removeprefix("gs://"),
        gcp_conn_id=gcp_con_id,
        destination_project_dataset_table=bigquery_dest_uri,
        impersonation_chain="knada-hyka@knada-gcp.iam.gserviceaccount.com",
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
        source_objects=oracle_table,
        source_format="csv"
    )

    delete_from_bucket = GoogleCloudStorageDeleteOperator(
        task_id="delete-from-bucket",
        bucket_name=os.getenv("AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER").removeprefix("gs://"),
        objects=[oracle_table],
        gcp_conn_id=gcp_con_id,
    )

    return oracle_to_bucket >> bucket_to_bq >> delete_from_bucket

with DAG('OracleToBigqueryOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:
    oracle_to_bq = oracle_to_bigquery(
        oracle_con_id="oracle_con",
        oracle_table="nada",
        gcp_con_id="google_con_different_project",
        bigquery_dest_uri="nada-dev-db2e.test.fra_oracle"
    )

    oracle_to_bq
