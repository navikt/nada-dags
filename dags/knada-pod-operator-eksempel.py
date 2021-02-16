from airflow import DAG
from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('test', start_date=days_ago(1), schedule_interval="*/5 * * * *") as dag:
    t1 = create_knada_nb_pod_operator(dag=dag,
                                      email="erik.vattekar@nav.no",
                                      name="knada-pod-operator",
                                      slack_channel="#kubeflow-cron-alerts",
                                      repo="navikt/nada-dags",
                                      nb_path="notebooks/Transformation.ipynb",
                                      namespace="nada",
                                      branch="main",
                                      log_output=True)

    t1
