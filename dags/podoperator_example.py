import os

from airflow import DAG
from airflow.utils.dates import days_ago
from kubernetes import client as k8s

from common.python_podop_factory import create_python_pod_operator

with DAG('pytho-operator', start_date=days_ago(1), schedule_interval=None) as dag:
    podop = create_python_pod_operator(
        name="python_pod_op",
        repo="navikt/nada-dags",
        script_path="notebooks/script.py",
        slack_channel="#kubeflow-cron-alerts",
        image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow:2023-03-08-d3684b7",
        retries=0,
    )
