import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from kubernetes import client as k8s
import logging

log: logging.log = logging.getLogger("airflow")
log.setLevel(logging.INFO)

with DAG('BashOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:

    os.environ['WORLD'] = 'Mars'

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='while true; do date; sleep 1; done'
    )

    t2 = BashOperator(
        task_id='bye_task',
        bash_command='echo "Bye $WORLD"',
        env={
            'WORLD': 'Earth'
        })

    t1 >> t2
