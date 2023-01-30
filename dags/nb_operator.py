from airflow import DAG

from airflow.utils.dates import days_ago
from kubernetes import client
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator
import os


with DAG('test-nb-operator', start_date=days_ago(1), schedule_interval="0 10 * * *") as dag:
    t1 = create_knada_nb_pod_operator(dag=dag,
                                      name="knada-pod-operator",
                                      slack_channel="#kubeflow-cron-alerts",
                                      repo="navikt/nada-dags",
                                      nb_path="notebooks/mynb.ipynb",
                                      retries=1,
                                      container_resources=client.V1ResourceRequirements(
                                          limits={"memory": "5G"}
                                      ),
                                      delete_on_finish=False,
                                      branch="main")

    t1
