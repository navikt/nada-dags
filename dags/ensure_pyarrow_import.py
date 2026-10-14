from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from time import time

def mycallable():
    import pyarrow
    print("Hello")


with DAG('PyarrowImportTest', start_date=days_ago(1), schedule="50 8 * * 1-5", catchup=False) as dag:    
    run_this = PythonOperator(
        dag=dag,
        task_id='egen-task-for-aa-teste-pyarrow-import',
        python_callable=mycallable,
    )
