import pandas as pd

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'start_date': datetime(2020, 10, 28)
}


def print_context():
    df = pd.DataFrame({"test": ["1", "2", "3"]})
    print(df)


with DAG('pythonoperatortest', default_args=default_args, schedule_interval=None) as dag:
    run_this = PythonOperator(
        task_id='test',
        python_callable=print_context,
        dag=dag
    )

    run_this