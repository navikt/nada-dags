from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from kubernetes import client as k8s
import time
import random


def mycallable():
    time.sleep(random.randrange(150))


with DAG("SimpleSlackTest", start_date=days_ago(1), schedule_interval=None) as dag:
    run_this = PythonOperator(
        task_id="test-pythonoperator",
        on_success_callback=[
            send_slack_notification(
                text="The DAG {{ run_id }} succeeded",
                channel="#nada-test",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
        on_failure_callback=[
            send_slack_notification(
                text="The DAG {{ run_id }} failed",
                channel="#nada-test",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
        python_callable=mycallable,
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"})
            )
        },
        dag=dag,
    )
