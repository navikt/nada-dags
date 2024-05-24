from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from kubernetes import client as k8s
import time


def mycallable():
    time.sleep(10)


with DAG("SlackOnSuccessOnFailureExample", start_date=days_ago(1), schedule="55 8 * * 1-5", catchup=False) as dag:
    run_this = PythonOperator(
        task_id="test-pythonoperator",
        on_success_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} succeeded",
                channel="#nada-test",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
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
