from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from kubernetes.client import models as k8s

with DAG('Papermill', start_date=datetime(2023, 3, 21), schedule=None) as dag:

    t1 = BashOperator(
        task_id='bashmill',
        bash_command='papermill --log-output /dags/notebooks/bashmill.ipynb /dags/notebooks/output.ipynb',
        executor_config={
           'pod_override': k8s.V1Pod(
               spec=k8s.V1PodSpec(
                   containers=[
                      k8s.V1Container(
                          name='base',
                          image='europe-north1-docker.pkg.dev/knada-gcp/knada/airflow-papermill:2023-08-31-ab6e198'
                      )
                   ]
               )
           )
        }
    )
