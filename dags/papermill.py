from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from datetime import datetime


with DAG('Papermill', start_date=datetime(2023, 3, 21), schedule="50 8 * * 1-5", catchup=False) as dag:

    t1 = BashOperator(
        task_id='bashmill',
        bash_command='papermill --log-output /dags/notebooks/bashmill.ipynb /dags/notebooks/output.ipynb',
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel="#nada-alerts-dev",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
    )
