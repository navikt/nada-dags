import os
from airflow import DAG
from airflow.providers.google.cloud.transfers.oracle_to_gcs import OracleToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.gcs_delete_operator import GoogleCloudStorageDeleteOperator
from datetime import datetime


def create_sql_delta_query(dag: DAG, oracle_table: str, delta_colum: str, num_rows: int):
    #next_from = dag.get_task_instances()
    return f"SELECT * FROM {oracle_table} FETCH NEXT {num_rows} ONLY"


def oracle_to_bigquery(
    dag: DAG,
    oracle_con_id: str,
    oracle_table: str,
    gcp_con_id: str,
    bigquery_dest_uri: str,
    num_rows: int = None,
    delta_column: str = None
):
    if num_rows and delta_column:
        write_disposition = "WRITE_APPEND"
        sql = create_sql_delta_query(dag, oracle_table, delta_column, num_rows)
    else:
        write_disposition = "WRITE_TRUNCATE"
        sql=f"SELECT * FROM {oracle_table}"

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

    # hent ut siste dato lastet til bq
    # skriv xcom

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
        oracle_table="nadairflow",
        gcp_con_id="google_con_different_project",
        bigquery_dest_uri="nada-dev-db2e.test.fra_oracle",
        num_rows=100,
        delta_column="date",
    )

    oracle_to_bq
