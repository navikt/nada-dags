from airflow import DAG
from datetime import datetime
import pendulum
from common.podop_factory import create_pod_operator
from kubernetes import client as k8s

with DAG(
    dag_id="InstallPackagesAtRuntime",
    description="dette er en pod operator som installerer python pakker ved oppstart",
    schedule_interval=None,
    start_date=datetime(2023, 1, 26, tzinfo=pendulum.timezone("Europe/Oslo")),
    catchup=False,
) as dag:
  podop = create_pod_operator(
    dag=dag, 
    name="task",
    repo="navikt/nada-dags",
    branch="main",
    quarto_path="notebooks/quarto.ipynb",
    delete_on_finish=False,
    requirements_file="notebooks/requirements.txt",
    image="europe-north1-docker.pkg.dev/knada-gcp/knada-north/airflow:2023-09-22-0bb59f1",
    slack_channel="#kubeflow-cron-alerts",
    resources=k8s.V1ResourceRequirements(
        requests={
            "memory": "256Mi"
        }
    )
  )
