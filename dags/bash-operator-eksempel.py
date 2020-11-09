from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'start_date': datetime(2020, 11, 9)
}

with DAG('bash-operator-eksempel', default_args=default_args, schedule_interval=None) as dag:
    t1 = BashOperator(
        task_id='hellotask',
        bash_command='echo "Hello world"',
        dag=dag)
    t2 = BashOperator(
        task_id='byetask',
        bash_command='echo "Bye world"',
        dag=dag)

    t1 >> t2
