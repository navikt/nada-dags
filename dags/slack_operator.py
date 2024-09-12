from airflow import DAG
from airflow.utils.dates import days_ago
from kubernetes import client as k8s
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
from airflow.operators.python import get_current_context
import os

with DAG('SlackOperator', start_date=days_ago(1), schedule="0 9 * * 1-5", catchup=False) as dag:
  slack_here_test = SlackAPIPostOperator(
            dag=dag,
            task_id="airflow_task_failed_slack",
            slack_conn_id="slack_connection",
            text=f"<!here> Airflow task feilet",
            channel="#kubeflow-cron-alerts",
    )
  
  slack = SlackAPIPostOperator(
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
  )
  slack_here_test >> slack
