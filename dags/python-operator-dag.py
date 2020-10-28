import pandas as pd
from airflow.operators.email_operator import EmailOperator

from dataverk_vault import api as vault_api
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'start_date': datetime(2020, 10, 28)
}


def print_context():
    vault_api.set_secrets_as_envs()
    df = pd.DataFrame({"test": ["1", "2", "3"]})
    print(df)


with DAG('pythonoperatortest', default_args=default_args, schedule_interval=None) as dag:
    run_this = PythonOperator(
        task_id='test',
        python_callable=print_context,
        dag=dag
    )

    t1 = EmailOperator(
        task_id="send_mail",
        to='erik.vattekar@nav.no',
        subject='Test mail',
        html_content='<p> You have got mail! <p>',
        dag=dag)

    run_this >> t1
