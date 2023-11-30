import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import get_current_context
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
from datetime import datetime
from kubernetes import client as k8s

def slack_success(context = None):
  if context is None: context = get_current_context()
  SlackAPIPostOperator(
    task_id="slack-success",
    slack_conn_id="slack_connection",
    text="suksess",
    channel="#kubeflow-cron-alerts",
  ).execute()

with DAG('OnSuccessCallbackTest',
        start_date=datetime(2023, 2, 14), 
        default_args={'on_success_callback': slack_success},
        schedule=None
) as dag:

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='echo "Hello $(date)"',
        executor_config = {
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "slack.com,hooks.slack.com"})
            )
        }
    )

    t2 = BashOperator(
        task_id='hello_task2',
        bash_command='echo "Hello $(date)"',
        executor_config = {
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "slack.com,hooks.slack.com"})
            )
        }
    )

    t1 >> t2
