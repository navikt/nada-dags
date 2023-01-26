from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from kubernetes import client as k8s
import os
import logging


def myfunc():
    logging.info("func")
    logging.warning("team secret path", os.environ["KNADA_TEAM_SECRET"])

with DAG('test-k8s-exec', start_date=days_ago(1), schedule_interval=None) as dag:
    executor_config_template={
        "pod_override": k8s.V1Pod(spec={"serviceAccountName": "flowtheair-49jg"})
    }
    
    run_this = PythonOperator(
    task_id='test',
    python_callable=myfunc,
    dag=dag)
