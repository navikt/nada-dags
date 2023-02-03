from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from kubernetes import client as k8s
import os
import logging


def myfunc():
    logging.info("func")
    logging.warning(f"team secret path {os.environ['KNADA_TEAM_SECRET']}")

with DAG('test-k8s-exec', start_date=days_ago(1), schedule_interval=None) as dag:
    slack = SlackWebhookOperator(
    http_conn_id=None,
    task_id="slack-message",
    webhook_token=os.environ["SLACK_TOKEN"],
    message=message,
    channel=channel,
    link_names=True,
    icon_emoji=emoji,
    attachments=attachments
    )
    
    run_this = PythonOperator(
    task_id='test',
    python_callable=myfunc,
    executor_config={
        "pod_override": k8s.V1Pod(
            metadata=k8s.V1ObjectMeta(labels={"mylabel": "value"}),
            spec=k8s.V1PodSpec(
                containers=[
                   k8s.V1Container(
                      name="base",
                      image="apache/airflow:2.5.1-python3.9",
                   )
                ]
            )
        )
    },
    dag=dag)
    slack > run_this
