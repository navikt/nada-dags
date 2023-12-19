import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('BashOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:

    os.environ['WORLD'] = 'Mars'

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='echo "Hello $WORLD at $(date)"',
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "35.235.240.1:89"})
            )
        }
    )

    t2 = BashOperator(
        task_id='bye_task',
        bash_command='echo "Bye $WORLD"',
        env={
            'WORLD': 'Earth'
        })

    t1 >> t2
