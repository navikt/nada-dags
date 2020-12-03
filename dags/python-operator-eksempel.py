import pandas as pd
import os

from dataverk_vault import api as vault_api
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def print_df():
    vault_api.set_secrets_as_envs()
    print(os.environ["TESTE"])
    df = pd.DataFrame({"test": ["1", "2", "3"]})
    print(df)


with DAG('python-operator-eksempel', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:

    os.environ["TESTE"] = "hallo - hallo - hallo"

    run_this = PythonOperator(
        task_id='test',
        python_callable=print_df,
        dag=dag)
