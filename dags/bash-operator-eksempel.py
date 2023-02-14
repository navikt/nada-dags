import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('bash-operator-eksempel', start_date=datetime(2023, 13, 2), schedule_interval="*/5 * * * *", catchup=False) as dag:

    os.environ["TEST"] = "hallo"

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='echo "$TEST world at ${date}"',
        dag=dag)
    t2 = BashOperator(
        task_id='bye_task',
        bash_command='echo "Bye world"',
        dag=dag)

    t1 >> t2
