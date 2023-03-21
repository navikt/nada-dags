from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('bash-operator-eksempel', start_date=datetime(2023, 2, 14), schedule_interval="*/5 * * * *", catchup=False) as dag:

    os.environ["TEST"] = "hallo"

    t1 = BashOperator(
        task_id='notebook',
        bash_command='papermill --log-output ../notebooks/mynb.ipynb ../output.ipynb',
        dag=dag)
