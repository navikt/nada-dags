from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from kubernetes import client as k8s
from time import time

def mycallable():
    print("hallo")

with DAG('PythonOperator', start_date=days_ago(1), schedule="50 8 * * 1-5", catchup=False) as dag:    
    run_this = PythonOperator(
        dag=dag,
        task_id='test-pythonoperator',
        python_callable=mycallable,
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"}),
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-papermill:2023-03-22-fb1c4a4",
                            working_dir="/dags/notebooks"
                        )
                    ]
                )
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
