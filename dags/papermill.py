from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from kubernetes.client import models as k8s

with DAG('Papermill', start_date=datetime(2023, 3, 21), schedule=None) as dag:

    t1 = BashOperator(
        task_id='bashmill',
        bash_command='sleep 1000 && papermill --log-output mynb.ipynb output.ipynb',
        executor_config={
           'pod_override': k8s.V1Pod(
               spec=k8s.V1PodSpec(
                   containers=[
                      k8s.V1Container(
                         name='base',
                         image='europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-papermill:2023-03-22-fb1c4a4',
                         working_dir="/dags/notebooks"
                      )
                   ]
               )
           )
        }
    )
