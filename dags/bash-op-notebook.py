from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from datetime import datetimefrom kubernetes import client as k8s
from airflow.utils.dates import days_ago


with DAG('bash-operator-notebook', start_date=days_ago(1), schedule_interval=None, catchup=False) as dag:

    t1 = BashOperator(
        task_id='notebook',
        bash_command='papermill --log-output ../notebooks/mynb.ipynb ../output.ipynb',
        executor_config={
           "pod_override": k8s.V1Pod(
               spec=k8s.V1PodSpec(
                   containers=[
                      k8s.V1Container(
                         name="base",
                         image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-notebooks:2023-03-21-ed0d1e5"
                      )
                   ]
               )
           )
        },
        dag=dag
    )
