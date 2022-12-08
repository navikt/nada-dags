from airflow import DAG

from airflow.utils.dates import days_ago
from kubernetes import client
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator
import os
from google.cloud import secretmanager
secrets = secretmanager.SecretManagerServiceClient()

resource_name = f"{os.environ['KNADA_TEAM_SECRET']}/versions/latest"
secret = secrets.access_secret_version(name=resource_name)
data = secret.payload.data.decode('UTF-8')


with DAG('test-nb-operator', start_date=days_ago(1), schedule_interval=None) as dag:
    t1 = create_knada_nb_pod_operator(dag=dag,
                                      name="knada-pod-operator",
                                      slack_channel="#kubeflow-cron-alerts",
                                      repo="navikt/nada-dags",
                                      nb_path="notebooks/mynb.ipynb",
                                      delete_on_finish=False,
                                      resources=client.V1ResourceRequirements(
                                          limits={"memory": "5G"}
                                      ),
                                      branch="main")

    t1
