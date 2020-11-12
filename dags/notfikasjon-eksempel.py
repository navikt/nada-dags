import os

from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime
from airflow import DAG


with DAG('notifikasjon-eksempel', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:
    email_notification = EmailOperator(
        dag=dag,
        task_id="send_email",
        to='erik.vattekar@nav.no',
        subject='Test mail',
        html_content='<p> You have got mail! <p>')

    slack_notification = SlackWebhookOperator(
        dag=dag,
        task_id="slack_notification_test",
        webhook_token=os.environ["SLACK_WEBHOOK_TOKEN"],
        message=f"Melding",
        channel="#kubeflow-cron-alerts",
        link_names=True,
        icon_emoji=":tada:",
        proxy=os.environ["HTTPS_PROXY"]
    )

    email_notification >> slack_notification
