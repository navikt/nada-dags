import pandas as pd

from dataverk_vault import api as vault_api
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def print_df():
    vault_api.set_secrets_as_envs()
    df = pd.DataFrame({"test": ["1", "2", "3"]})
    print(df)


with DAG('python-operator-eksempel', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:
    run_this = PythonOperator(
        task_id='test',
        python_callable=print_df,
        dag=dag
    )
