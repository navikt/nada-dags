from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
import os

with DAG('slack-operator', start_date=days_ago(1), schedule_interval=None) as dag:   
  slack = SlackAPIPostOperator(
    task_id="error",
    dag=dag,
    token=os.environ["SLACK_TOKEN"],
    text="tester",
    channel="#kubeflow-cron-alerts",
    attachments=[
      {
          "fallback": "Plain-text summary of the attachment.",
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
  )
