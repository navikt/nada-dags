from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_dbt_seed_operator, create_knada_dbt_run_operator

with DAG('dbt-bigquery-eksempel', start_date=days_ago(0), schedule_interval=None) as dag:
    seed_gcs = create_knada_dbt_seed_operator(dag,
                                              name="seed-gcs-blob",
                                              repo="navikt/nada-dags",
                                              namespace="nada",
                                              dbt_dir="styrk",
                                              seed_source={"host": "gcs",
                                                           "gcs_bucket": "styrk-bucket",
                                                           "blob_name": "styrk-koder/styrk.csv"},
                                              email="erik.vattekar@nav.no",
                                              branch="main")

    dbt_run = create_knada_dbt_run_operator(dag,
                                            name="dbt-run",
                                            repo="navikt/nada-dags",
                                            namespace="nada",
                                            dbt_dir="styrk",
                                            email="erik.vattekar@nav.no",
                                            branch="main")

    seed_gcs >> dbt_run
