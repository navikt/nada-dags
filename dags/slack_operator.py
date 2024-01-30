from airflow import DAG
from airflow.utils.dates import days_ago
from kubernetes import client as k8s
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
from airflow.operators.python import get_current_context
import os

def slack_message():
  SlackAPIPostOperator(
    task_id="error",
    dag=dag,
    executor_config={
      "pod_override": k8s.V1Pod(
          metadata=k8s.V1ObjectMeta(annotations={"allowlist": "slack.com"})
      )
    },
    slack_conn_id="slack_connection",
    text=":red_circle: tester",
    channel="#kubeflow-cron-alerts",
    attachments=[
      {
          "fallback": "min attachment",
          "color": "#2eb886",
          "pretext": "test",
          "author_name": "Nada",
          "title": "Nada",
          "text": "test",
          "fields": [
              {
                  "title": "Priority",
                  "value": "High",
                  "short": False
              }
          ],
          "footer": "Nada"
      }
    ]
  ).execute(context=get_current_context())

with DAG('SlackOperator', start_date=days_ago(1), schedule_interval=None) as dag:

  slack_message = slack_message()
