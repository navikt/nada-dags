from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('oracle-to-gcs', start_date=days_ago(1), schedule_interval="0 0 * * *") as dag:
    oracle_to_gcs = create_knada_nb_pod_operator(dag=dag,
                                                 name="oracle-to-gcs",
                                                 repo="navikt/nada-dags",
                                                 nb_path="notebooks/MigrateOracleToGCS.ipynb",
                                                 email="erik.vattekar@nav.no",
                                                 slack_channel="#kubeflow-cron-alerts",
                                                 namespace="nada",
                                                 branch="main",
                                                 log_output=False,
                                                 retries=3,
                                                 retry_delay=timedelta(seconds=5))
