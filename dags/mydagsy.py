from airflow import DAG

from airflow.utils.dates import days_ago
from kubernetes import client
from dataverk_airflow.knada_operators import create_knada_python_pod_operator
import os

os.environ["KNADA_NOTEBOOK_OP_IMAGE"] = "ghcr.io/navikt/knada-airflow:2022-12-15-d6ba810"

with DAG('test-python-operator', start_date=days_ago(1), schedule_interval=None) as dag:
    t1 = create_knada_python_pod_operator(dag=dag,
                                      name="knada-python-operator",
                                      repo="navikt/nada-dags",
                                      script_path="notebooks/script.py",
                                      delete_on_finish=False,
                                      resources=client.V1ResourceRequirements(
                                          limits={"memory": "128M"}
                                      ),
                                      branch="main")

    t1
