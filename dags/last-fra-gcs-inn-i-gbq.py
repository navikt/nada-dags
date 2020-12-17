from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_bq_operator

with DAG('last-fra-gcs-inn-i-bigquery', start_date=days_ago(0), schedule_interval=None) as dag:
    load_from_gcs_bucket_into_gbq = create_knada_bq_operator(dag,
                                                             name="bq-load",
                                                             namespace="nada",
                                                             bq_cmd="bq load --source_format=PARQUET dbt_demo.styrk_gcs "
                                                                    "gs://styrk-bucket/styrk-koder/styrk.gzip",
                                                             email="erik.vattekar@nav.no")
