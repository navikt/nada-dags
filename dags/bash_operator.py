import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from kubernetes import client as k8s
from datetime import datetime

with DAG('BashOperator', start_date=datetime(2023, 2, 14), schedule="0 8 * * 1-5", catchup=False) as dag:

    os.environ['WORLD'] = 'Mars'

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='echo "Hello Earth"',
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"})
            )
        },
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
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
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"})
            )
        },
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel="#nada-alerts-dev",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ]
        )

    t1 >> t2
