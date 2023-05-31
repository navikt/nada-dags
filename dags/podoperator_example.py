import os

from airflow import DAG
from airflow.utils.dates import days_ago
from kubernetes import client as k8s

from common.podop_factory import create_pod_operator

with DAG('pod-operator-examples', start_date=days_ago(1), schedule_interval=None) as dag:
    podop_script = create_pod_operator(
        dag=dag,
        name="python_pod_op",
        repo="navikt/nada-dags",
        script_path="notebooks/script.py",
        slack_channel="#kubeflow-cron-alerts",
        image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow:2023-03-08-d3684b7",
        retries=0,
        delete_on_finish=False,
    )

    podop_nb = create_pod_operator(
        dag=dag,
        name="nb_pod_op",
        repo="navikt/nada-dags",
        nb_path="notebooks/mynb.ipynb",
        slack_channel="#kubeflow-cron-alerts",
        
        retries=0,
        delete_on_finish=False,
    )

    podop_script >> podop_nb
