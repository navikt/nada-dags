from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_dbt_seed_operator

with DAG('dtp-bigquery-eksempel', start_date=days_ago(0), schedule_interval=None) as dag:
    seed_gcs = create_knada_dbt_seed_operator(dag,
                                              name="seed-gcs-bucket",
                                              repo="navikt/nada-dags",
                                              namespace="nada",
                                              dbt_dir="styrk",
                                              seed_source={"gcs_bucket": "styrk-bucket",
                                                           "blob_name": "styrk-kode/styrk.csv"},
                                              delete_on_finish=False,
                                              email="erik.vattekar@nav.no",
                                              branch="main")
