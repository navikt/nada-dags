from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'start_date': datetime(2019, 4, 1)
}

with DAG('eksempel', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    t1 = BashOperator(
        task_id='hellotask',
        bash_command='echo "Hello world"',
        dag=dag)
    t2 = BashOperator(
        task_id='byetask',
        bash_command='echo "Bye world"',
        dag=dag)

    t1 >> t2
