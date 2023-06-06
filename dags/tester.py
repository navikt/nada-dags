import os
from datetime import datetime, timedelta, date
from airflow.utils.dates import days_ago
from airflow import DAG
from common.podop_factory import create_pod_operator
from kubernetes import client

dag_name = 'test_xcom'

# default_args = {
#     'owner': 'erik',
#     'start_date': datetime(2023, 6, 6),
#     # 'depends_on_past': False,
#     # If a task fails, retry it once after waiting at least 5 minutes
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }


with DAG(dag_name, start_date=days_ago(1), schedule_interval=None) as dag:

    test_task = create_pod_operator(
        dag=dag,
        name='test_task',
        repo='navikt/nada-dags',
        nb_path='test_notebook.ipynb',
        slack_channel="#kubeflow-cron-alerts",
        branch='main',
        do_xcom_push = True,
        resources=client.V1ResourceRequirements(
            requests={"memory": "512Mi"}
        )
    )


test_task