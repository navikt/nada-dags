from airflow import DAG
from datetime import datetime
import pendulum
from dataverk_airflow import quarto_operator
from airflow.models import Variable
from kubernetes import client as k8s

with DAG(
    dag_id="QuartoWithInstallPackagesAtRuntime",
    description="Dette er en pod operator som installerer python pakker ved oppstart og publiserer en quarto fortelling",
    schedule_interval=None,
    start_date=datetime(2023, 1, 26, tzinfo=pendulum.timezone("Europe/Oslo")),
    catchup=False,
) as dag:
  quarto = quarto_operator(
    dag=dag,
    name="task",
    repo="navikt/nada-dags",
    branch="main",
    quarto={
        "path": "notebooks/quarto.ipynb",
        "env": "data.ekstern.dev.nav.no",
        "id": "2512b49d-dbfa-48d9-9f18-0d077517706a",
        "token": Variable.get("quarto_token"),
    },
    requirements_path="notebooks/requirements.txt",
    slack_channel="#kubeflow-cron-alerts",
    resources=k8s.V1ResourceRequirements(
        requests={
            "memory": "256Mi"
        }
    )
  )
