from airflow import DAG
from airflow.utils.dates import days_ago
from airflow_dbt import DbtRunOperator
from dataverk_airflow.knada_operators import create_knada_dbt_seed_operator

with DAG('dtp-bigquery-eksempel', start_date=days_ago(0), schedule_interval=None) as dag:
    seed_gcs = create_knada_dbt_seed_operator(dag,
                                              name="seed-gcs-blob",
                                              repo="navikt/nada-dags",
                                              namespace="nada",
                                              dbt_dir="styrk",
                                              seed_source={"gcs_bucket": "styrk-bucket",
                                                           "blob_name": "styrk-koder/styrk.csv"},
                                              email="erik.vattekar@nav.no",
                                              branch="main")

    dtp_run = DbtRunOperator(task_id='dbt-run')

    seed_gcs >> dtp_run
