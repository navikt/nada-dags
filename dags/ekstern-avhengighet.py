from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.utils.dates import days_ago


with DAG('ekstern-avhengighet', start_date=days_ago(1), schedule_interval="10 14 * * *") as dag:
    task = ExternalTaskSensor(
        external_dag_id="bash-operator-eksempel",
        task_id="wait-for-external-task-completion"
    )

    t2 = BashOperator(
        task_id='test',
        bash_command='echo "test"',
        dag=dag
    )

    task >> t2
