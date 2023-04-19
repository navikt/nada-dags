import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from datetime import datetime
from datetime import datetime
from airflow.utils.dates import days_ago
from kubernetes import client as k8s

def on_failure(context):
    slack_notification = SlackWebhookOperator(
        http_conn_id=None,
        task_id="slack-message",
        webhook_token=os.environ["SLACK_TOKEN"],
        message="dag feiler",
        channel="#kubeflow-cron-alerts",
        link_names=True,
        executor_config={
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"})
            )
        }
    )

    slack_notification.execute(context)

with DAG('bash-operator-notebook', start_date=days_ago(1), schedule_interval=None, catchup=False) as dag:

    t1 = BashOperator(
        task_id='notebook',
        bash_command='papermill --log-output /dags/notebooks/mynb.ipynb /dags/output.ipynb',
        on_failure_callback=on_failure,
        on_execute_callback=on_failure,
        executor_config={
           "pod_override": k8s.V1Pod(
               spec=k8s.V1PodSpec(
                   containers=[
                      k8s.V1Container(
                         name="base",
                         image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-notebooks:manuel2"
                      )
                   ]
               )
           )
        },
        dag=dag
    )
