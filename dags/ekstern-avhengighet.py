from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor


with DAG('ekstern-avhengighet', start_date=datetime(2020, 11, 9), schedule_interval="55 14 * * *", catchup=False) as dag:
    task = ExternalTaskSensor(
        external_dag_id="bash-operator-eksempel",
        #external_task_id="byetask",
        task_id="wait-for-external-task-completion"
    )

    t2 = BashOperator(
        task_id='test',
        bash_command='echo "test"',
        dag=dag
    )

    task >> t2
