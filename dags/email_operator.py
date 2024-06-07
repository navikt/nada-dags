from airflow import DAG
from airflow.operators.email import EmailOperator
from datetime import datetime
from kubernetes import client as k8s
from airflow.providers.slack.notifications.slack import send_slack_notification


with DAG(dag_id="EmailOperator", start_date=datetime(2023, 2, 21), schedule="25 8 * * 1-5", catchup=False) as dag:
    epost = EmailOperator(
        task_id="send-epost",
        to=["erik.vattekar@nav.no"],
        subject="Hei, fra Airflow",
        html_content="<h1>Hello world</h1><p>Dette er en e-post sendt fra en Airflow DAG</p>",
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "smtp.adeo.no:26, 35.235.240.1:89, 35.235.240.2, hooks.slack.com"})
            )
        },
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel="#nada-alerts",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
    )
