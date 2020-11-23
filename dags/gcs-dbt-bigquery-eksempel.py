from airflow import DAG
from datetime import timedelta
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator
from airflow.utils.dates import days_ago


with DAG('gcs-dbt-bigquery-eksempel', start_date=days_ago(0), schedule_interval=None) as dag:
    task = create_knada_nb_pod_operator(dag=dag,
                                        name="read-ssb-write-gcs",
                                        repo="navikt/nada-dags",
                                        nb_path="notebooks/FetchStyrkUploadGCS",
                                        email="erik.vattekar@nav.no",
                                        namespace="nada",
                                        branch="main",
                                        log_output=True,
                                        retries=1,
                                        retry_delay=timedelta(seconds=5))
