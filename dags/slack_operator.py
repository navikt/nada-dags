from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
import os

with DAG('slack-operator', start_date=days_ago(1), schedule_interval=None) as dag:   
  slack = SlackWebhookOperator(
          task_id="airflow_task_failed",
          http_conn_id=None,
          webhook_token=os.environ["SLACK_TOKEN"],
          message=f"@here Airflow task i DAG feilet",
          channel="#kubeflow-cron-alerts",
          link_names=True,
          icon_emoji=":sadpanda:",
      )
