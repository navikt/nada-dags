from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime

def get_test_variable():
    test_value = Variable.get("test_variable")
    print(f"Value of test_variable: {test_value}")

with DAG('test_gcp_secret_manager',
         default_args={'owner': 'airflow', 'start_date': datetime(2023, 1, 1)},
         schedule_interval=None) as dag:

    test_task = PythonOperator(
        task_id='test_variable_access',
        python_callable=get_test_variable
    )
