from airflow import DAG

from airflow.utils.dates import days_ago
from kubernetes import client
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('test-nb-operator', start_date=days_ago(1), schedule_interval=None) as dag:
    t1 = create_knada_nb_pod_operator(dag=dag,
                                      name="knada-pod-operator",
                                      slack_channel="#kubeflow-cron-alerts",
                                      repo="navikt/nada-dags",
                                      nb_path="notebooks/mynb.ipynb",
                                      delete_on_finish=False,
                                      resources=client.V1ResourceRequirements(
                                          requests={"cpu": "1000m", "memory": "5G"},
                                          limits={"cpu": "2000m", "memory": "5G"}
                                      ),
                                      branch="main")

    t1
