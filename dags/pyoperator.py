from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from kubernetes import client as k8s
import os

def mycallable():
    print("hello")

with DAG('pytho-operator', start_date=days_ago(1), schedule_interval=None) as dag:    
    run_this = PythonOperator(
    task_id='test-pythonoperator',
    python_callable=mycallable,
    executor_config={
        "pod_override": k8s.V1Pod(
            spec=k8s.V1PodSpec(
                containers=[
                   k8s.V1Container(
                      name="base",
                      image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-papermill:2023-03-22-fb1c4a4"
                   )
                ]
            )
        )
    },
    dag=dag)
