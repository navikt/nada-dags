from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
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
    message="asdf",
    channel="#kubeflow-cron-alerts",
    link_names=True
    )
    
    run_this = PythonOperator(
    task_id='test',
    python_callable=myfunc,
    wait_for_downstream=False,
    provide_context=True,
    dag=dag)
    slack >> run_this
