from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
import os

with DAG('SlackOperator', start_date=days_ago(1), schedule_interval=None) as dag:   
  slack = SlackAPIPostOperator(
    task_id="error",
    dag=dag,
    slack_conn_id="slack-connection",
    # token=os.environ["SLACK_TOKEN"],
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
  )
