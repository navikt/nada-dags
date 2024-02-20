import os
from airflow import DAG
from airflow.providers.google.cloud.transfers.oracle_to_gcs import OracleToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.gcs_delete_operator import GoogleCloudStorageDeleteOperator
from kubernetes import client as k8s
from datetime import datetime


def oracle_to_bigquery(
    oracle_con_id: str,
    oracle_table: str,
    bucket_name: str,
    gcp_con_id: str,
    bigquery_dest_uri: str,
    columns: list = [],
):
    columns = ",".join(columns) if len(columns) > 0 else "*"
    write_disposition = "WRITE_TRUNCATE"
    sql=f"SELECT {columns} FROM {oracle_table}"

    oracle_to_bucket = OracleToGCSOperator(
        task_id="oracle-to-bucket",
        oracle_conn_id=oracle_con_id,
        gcp_conn_id=gcp_con_id,
        impersonation_chain=f"{os.getenv('TEAM')}@knada-gcp.iam.gserviceaccount.com",
        sql=sql,
        bucket=bucket_name,
        filename=oracle_table,
        export_format="csv",
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "dm07-scan.adeo.no:1521"})
            )
        }
    )

    bucket_to_bq = GCSToBigQueryOperator(
        task_id="bucket-to-bq",
        bucket=bucket_name,
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
        bucket_name=bucket_name,
        objects=[oracle_table],
        gcp_conn_id=gcp_con_id,
    )

    return oracle_to_bucket >> bucket_to_bq >> delete_from_bucket


# Følgende forutsetninger gjelder for å kunne ta i bruk SimpleOracleToBigqueryOperator:
# - Det må lages en bucket i samme teamprosjekt på GCP som bigquery tabellen skal ende opp
# - Det må lages et BigQuery datasett som tabellen skal skrives til
# - Service accounten til knada-teamet ditt må gis nødvendige tilganger i teamprosjekt for å skrive til bucket og bigquery
#   - Service accounten må få rollen BigQuery Job User på prosjektnivå for å kunne gjøre spørringer i prosjektet
#   - Service accounten må få rollen Storage Admin på storage bucketen i teamprosjektet
#   - Service accounten må få rollen BigQuery Admin på datasettet i teamprosjektet
# - Det må opprettes en oracle connection i Airflow UIet
#   - Velg Connection type 'Oracle'
#   - Legg til host, port, login (brukernavn) og password for koblingen
#   - Under extra så må service_name spesifiseres. Dette spesifiseres som en json, f.eks. {"service_name": "dwh"}
# - Det må opprettes en google connection i Airflow UIet
#   - Velg Connection type 'Google Cloud'
#   - Spesifiser kun 'project ID'. Dette settes til IDen til teamprosjektet med bucketen og bigquery datasettet
with DAG('SimpleOracleToBigqueryOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:
    oracle_to_bq = oracle_to_bigquery(
        oracle_con_id="oracle_con",
        oracle_table="nada",
        bucket_name="min-bucket-for-mellomlagring",
        gcp_con_id="google_con_different_project",
        bigquery_dest_uri="nada-dev-db2e.test.fra_oracle",
    )

    oracle_to_bq
