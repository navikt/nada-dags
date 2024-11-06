import sys
from airflow import DAG
from airflow.models import Variable
from airflow.providers.google.cloud.transfers.oracle_to_gcs import OracleToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.gcs_delete_operator import GoogleCloudStorageDeleteOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from kubernetes import client as k8s
from datetime import datetime

import sqlalchemy
import oracledb
oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb


# Oracle config
oracle_user = Variable.get('ORACLE_DB_USER')
oracle_pass = Variable.get('ORACLE_DB_PASSWORD')
oracle_host = Variable.get('ORACLE_DB_HOST')
oracle_port = Variable.get('ORACLE_DB_PORT')
oracle_table_name = Variable.get('ORACLE_DB_TABLE_NAME')
oracle_service_name = Variable.get('ORACLE_DB_SERVICE_NAME')

# Eposten til service accounten til knada-teamet ditt, denne finner du i knorten
# TODO: Kanskje automatisk injectes som miljøvariabel i alle airflow-worker containere i stedet?
knada_service_account_email = Variable.get('KNADA_SERVICE_ACCOUNT_EMAIL')


def create_oracle_table_and_prepopulate_with_data():
    engine = sqlalchemy.create_engine(f"oracle://{oracle_user}:{oracle_pass}@{oracle_host}:{oracle_port}/?service_name={oracle_service_name}")
    with engine.connect() as con:
        try:
            con.execute(sqlalchemy.text(f"drop table {oracle_table_name}"))
        except:
            pass
        con.execute(sqlalchemy.text(f"create table {oracle_table_name} (value number not null, column2 varchar2(10))"))
        con.execute(sqlalchemy.text(f"insert into {oracle_table_name} (value,column2) VALUES (1, 'test')"))
        con.execute(sqlalchemy.text("commit"))


def oracle_to_bigquery(
    oracle_con_id: str,
    oracle_table: str,
    bucket_name: str,
    gcp_con_id: str,
    bigquery_dest_uri: str,
    slack_channel: str = None,
    columns: list = [],
):
    columns = ",".join(columns) if len(columns) > 0 else "*"
    write_disposition = "WRITE_TRUNCATE"
    sql=f"SELECT {columns} FROM {oracle_table}"

    oracle_to_bucket = OracleToGCSOperator(
        task_id="oracle-to-bucket",
        oracle_conn_id=oracle_con_id,
        gcp_conn_id=gcp_con_id,
        impersonation_chain=f"{knada_service_account_email}",
        sql=sql,
        bucket=bucket_name,
        filename=oracle_table,
        export_format="csv",
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": f"{oracle_host}:{oracle_port},hooks.slack.com"})
            )
        },
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel=slack_channel,
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ] if slack_channel else [],
    )

    bucket_to_bq = GCSToBigQueryOperator(
        task_id="bucket-to-bq",
        bucket=bucket_name,
        gcp_conn_id=gcp_con_id,
        destination_project_dataset_table=bigquery_dest_uri,
        impersonation_chain=f"{knada_service_account_email}",
        autodetect=True,
        write_disposition=write_disposition,
        source_objects=oracle_table,
        source_format="csv",
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"})
            )
        },
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel=slack_channel,
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ] if slack_channel else [],
    )

    delete_from_bucket = GoogleCloudStorageDeleteOperator(
        task_id="delete-from-bucket",
        bucket_name=bucket_name,
        objects=[oracle_table],
        gcp_conn_id=gcp_con_id,
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"})
            )
        },
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel=slack_channel,
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ] if slack_channel else [],
    )

    return oracle_to_bucket, bucket_to_bq, delete_from_bucket


# Følgende forutsetninger gjelder for å kunne ta i bruk OracleToBigqueryOperator:
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
with DAG('OracleToBigqueryOperator', start_date=datetime(2023, 2, 14), schedule="45 8 * * 1-5", catchup=False) as dag:

    # Dette første steget oppretter en tabell med data i Oracle som vi kan bruke i eksempelet som flytter data til bigquery nedenfor.
    # Dersom du allerede har en tabell i Oracle med data kan du hoppe over dette steget.
    create_table_with_data = PythonOperator(
        dag=dag,
        task_id="create-oracle-table-and-prepopulate-with-data",
        python_callable=create_oracle_table_and_prepopulate_with_data,
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"}),
            )
        },
        # on_failure_callback=[
        #     send_slack_notification(
        #         text="{{ task }} run {{ run_id }} of {{ dag }} failed",
        #         channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
        #         slack_conn_id="slack_connection",
        #         username="Airflow",
        #     )
        # ],
    )

    # Dette steget kopierer data fra Oracle til en bucket i GCS og deretter til BigQuery
    oracle_to_bucket, bucket_to_bq, delete_from_bucket = oracle_to_bigquery(
        oracle_con_id="oracle_con",
        oracle_table=oracle_table_name,
        bucket_name="nada-airflow-tests",
        gcp_con_id="google_con_different_project",
        bigquery_dest_uri=f"nada-prod-6977.airflow_integration_tests.fra_oracle_+{oracle_table_name}",
        #slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
    )

    create_table_with_data >> oracle_to_bucket >> bucket_to_bq >> delete_from_bucket
