from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_dbt_seed_operator

with DAG('last-fra-onprem-s3-inn-i-gbq', start_date=days_ago(0), schedule_interval=None) as dag:
    seed_s3 = create_knada_dbt_seed_operator(dag,
                                             name="seed-s3-blob",
                                             repo="navikt/bq-dags",
                                             namespace="nada",
                                             dbt_dir="styrk",
                                             seed_source={"host": "s3",
                                                          "bucket": "nav-opendata",
                                                          "blob_name": "styrk-koder/styrk_s3.csv"},
                                             email="erik.vattekar@nav.no",
                                             branch="main")
