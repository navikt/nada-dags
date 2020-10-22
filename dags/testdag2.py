from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'start_date': datetime(2019, 4, 1)
}

with DAG('eriktester', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    t1 = BashOperator(
        task_id='erik',
        bash_command='echo "Erik"',
        dag=dag)
    t2 = BashOperator(
        task_id='tester',
        bash_command='echo "tester"',
        dag=dag)

    t1 >> t2
