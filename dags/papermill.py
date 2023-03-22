from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.providers.papermill.operators.papermill import PapermillOperator
from datetime import datetime
from kubernetes.client import models as k8s

dockerImage = 'europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-papermill:2023-03-22-8018f16'

with DAG('Papermill', start_date=datetime(2023, 3, 21), schedule_interval='0 10 * * *') as dag:

    t1 = BashOperator(
        task_id='bashmill',
        bash_command='papermill --log-output /dags/notebooks/mynb.ipynb /dags/output.ipynb',
        executor_config={
           'pod_override': k8s.V1Pod(
               spec=k8s.V1PodSpec(
                   containers=[
                      k8s.V1Container(
                         name='base',
                         image=dockerImage
                      )
                   ]
               )
           )
        }
    )
    
    t2 = KubernetesPodOperator(
        task_id='podmill',
        image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-papermill-test:1",
        arguments=[
            '--log-output',
            '/dags/notebooks/mynb.ipynb',
            '/dags/output.ipynb'
        ]
    )

    t3 = PapermillOperator(
        task_id="run_example_notebook",
        input_nb="/dags/notebooks/mynb.ipynb",
        output_nb="/dags/out-{{ execution_date }}.ipynb",
        parameters={"msgs": "Ran from Airflow at {{ execution_date }}!"},
    )
