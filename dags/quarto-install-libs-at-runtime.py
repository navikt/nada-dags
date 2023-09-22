from airflow import DAG
from datetime import datetime
import pendulum
from common.podop_factory import create_pod_operator
from airflow.models import Variable
from kubernetes import client as k8s

with DAG(
    dag_id="QuartoWithInstallPackagesAtRuntime",
    description="Dette er en pod operator som installerer python pakker ved oppstart og publiserer en quarto fortelling",
    schedule_interval=None,
    start_date=datetime(2023, 1, 26, tzinfo=pendulum.timezone("Europe/Oslo")),
    catchup=False,
) as dag:
  podop = create_pod_operator(
    dag=dag, 
    name="task",
    repo="navikt/nada-dags",
    branch="main",
    quarto={
        "path": "notebooks/quarto.ipynb",
        "environment": "data.ekstern.dev.nav.no",
        "id": "2512b49d-dbfa-48d9-9f18-0d077517706a",
        "token": Variable.get("quarto_token"),
    },
    requirements_file="notebooks/requirements.txt",
    image="europe-north1-docker.pkg.dev/knada-gcp/knada-north/airflow:2023-09-22-0bb59f1",
    delete_on_finish=False,
    slack_channel="#kubeflow-cron-alerts",
    resources=k8s.V1ResourceRequirements(
        requests={
            "memory": "256Mi"
        }
    )
  )
