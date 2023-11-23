import os
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.providers.google.cloud.transfers.oracle_to_gcs import OracleToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.gcs_delete_operator import GoogleCloudStorageDeleteOperator
from datetime import datetime


def oracle_to_bigquery(
    oracle_con_id: str,
    oracle_table: str,
    gcp_con_id: str,
    bigquery_dest_uri: str,
    columns: list = None,
    num_rows: int = None,
    delta_column: str = None
):
    columns = ",".join(columns) if len(columns) > 0 else "*"

    if num_rows and delta_column:
        offset_variable = "offset-"+oracle_table
        try:
            offset = Variable.get(offset_variable)
        except KeyError:
            offset = 0
        write_disposition = "WRITE_APPEND"
        sql = f"SELECT {columns} FROM {oracle_table} ORDER BY {delta_column} OFFSET {offset} ROWS FETCH NEXT {num_rows} ROWS ONLY"
    else:
        write_disposition = "WRITE_TRUNCATE"
        sql=f"SELECT {columns} FROM {oracle_table}"

    oracle_to_bucket = OracleToGCSOperator(
        task_id="oracle-to-bucket",
        oracle_conn_id=oracle_con_id,
        gcp_conn_id=gcp_con_id,
        impersonation_chain=f"{os.getenv('TEAM')}@knada-gcp.iam.gserviceaccount.com",
        sql=sql,
        bucket=os.getenv("AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER").removeprefix("gs://"),
        filename=oracle_table,
        export_format="csv"
    )

    bucket_to_bq = GCSToBigQueryOperator(
        task_id="bucket-to-bq",
        bucket=os.getenv("AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER").removeprefix("gs://"),
        gcp_conn_id=gcp_con_id,
        destination_project_dataset_table=bigquery_dest_uri,
        impersonation_chain=f"{os.getenv('TEAM')}@knada-gcp.iam.gserviceaccount.com",
        autodetect=True,
        write_disposition=write_disposition,
        source_objects=oracle_table,
        source_format="csv"
    )

    delete_from_bucket = GoogleCloudStorageDeleteOperator(
        task_id="delete-from-bucket",
        bucket_name=os.getenv("AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER").removeprefix("gs://"),
        objects=[oracle_table],
        gcp_conn_id=gcp_con_id,
    )

    if num_rows and delta_column:
        update_offset = BashOperator(
            task_id='update-offset',
            bash_command=f"airflow variables set {offset_variable} {int(offset) + num_rows}"
        )

        return oracle_to_bucket >> bucket_to_bq >> [delete_from_bucket, update_offset]

    return oracle_to_bucket >> bucket_to_bq >> delete_from_bucket


with DAG('OracleToBigqueryOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:
    oracle_to_bq = oracle_to_bigquery(
        oracle_con_id="oracle_con",
        oracle_table="nada",
        gcp_con_id="google_con_different_project",
        bigquery_dest_uri="nada-dev-db2e.test.fra_oracle",
        num_rows=1000,
        delta_column="id",
    )

    oracle_to_bq
