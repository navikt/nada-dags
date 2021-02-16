from airflow import DAG
from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('knada-pod-operator-eksempel', start_date=days_ago(1), schedule_interval="*/5 * * * *") as dag:
    task = create_knada_nb_pod_operator(dag=dag,
                                        name="knada-pod-operator",
                                        repo="navikt/nada-dags",
                                        nb_path="notebooks/Transformation.ipynb",
                                        email="erik.vattekar@nav.no",
                                        slack_channel="#kubeflow-cron-alerts",
                                        namespace="nada",
                                        branch="main",
                                        log_output=True,
                                        retries=1,
                                        retry_delay=timedelta(seconds=5))
