import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('bash-operator-eksempel', start_date=datetime(2020, 11, 9), schedule_interval="3 15 * * *", catchup=False) as dag:

    os.environ["TEST"] = "hallo"

    t1 = BashOperator(
        task_id='hellotask',
        bash_command='echo "$TEST"',
        dag=dag)
    t2 = BashOperator(
        task_id='byetask',
        bash_command='echo "Bye world"',
        dag=dag)

    t1 >> t2
