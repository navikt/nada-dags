from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG('Papermill', start_date=datetime(2023, 3, 21), schedule=None) as dag:

    t1 = BashOperator(
        task_id='bashmill',
        bash_command='papermill --log-output /dags/notebooks/bashmill.ipynb /dags/notebooks/output.ipynb',
    )
