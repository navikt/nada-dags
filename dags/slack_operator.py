from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
import os

with DAG('slack-operator', start_date=days_ago(1), schedule_interval=None) as dag:   
  slack = SlackAPIPostOperator(
    task_id="error",
    dag=dag,
    token=os.environ["SLACK_TOKEN"],
    text="tester",
    channel="#kubeflow-cron-alerts",
  )
