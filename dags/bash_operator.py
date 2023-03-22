import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('BashOperator', start_date=datetime(2023, 2, 14), schedule_interval='*/5 * * * *', catchup=False) as dag:

    os.environ['WORLD'] = 'Mars'

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='echo 'Hello $WORLD at $(date)''
    )

    t2 = BashOperator(
        task_id='bye_task',
        bash_command='echo 'Bye $WORLD'',
        env={
            'WORLD': 'Earth'
        })

    t1 >> t2
