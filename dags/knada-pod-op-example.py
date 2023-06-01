from airflow import DAG
from datetime import datetime
import pendulum
from dataverk_airflow.knada_operators import create_knada_python_pod_operator
from kubernetes import client as k8s

with DAG(
    dag_id="pod-operator",
    description="dette er en pod operator",
    schedule_interval=None,
    start_date=datetime(2023, 1, 26, tzinfo=pendulum.timezone("Europe/Oslo")),
    catchup=False,
) as dag:
  podop = create_knada_python_pod_operator(
              dag=dag, 
              name="task",
              repo="navikt/nada-dags",
              branch="main",
              script_path="notebooks/script.py",
              delete_on_finish=False,
              slack_channel="#kubeflow-cron-alerts",
              retries=1,
              do_xcom_push=True,
              resources=k8s.V1ResourceRequirements(
                  requests={
                      "memory": "50Mi"
                  }
              )
  )
