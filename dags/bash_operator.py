import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from datetime import datetime

with DAG('BashOperator', start_date=datetime(2023, 2, 14), schedule="0 8 * * 1-5", catchup=False) as dag:

    os.environ['WORLD'] = 'Mars'

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='echo "Hello Earth"',
        on_success_callback=[
            send_slack_notification(
                text="The DAG {{ run_id }} succeeded",
                channel="#nada-alerts-dev",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
        on_failure_callback=[
            send_slack_notification(
                text="The DAG {{ run_id }} failed",
                channel="#nada-alerts-dev",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
    )

    t2 = BashOperator(
        task_id='bye_task',
        bash_command='echo "Bye $WORLD"',
        env={
            'WORLD': 'Earth'
        },
        on_failure_callback=[
            send_slack_notification(
                text="The DAG {{ run_id }} failed",
                channel="#nada-alerts-dev",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ]
        )

    t1 >> t2
