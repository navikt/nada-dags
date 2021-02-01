import os
from datetime import timedelta
from airflow import DAG
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('ge-rapport-varsling', start_date=days_ago(1), schedule_interval=None) as dag:
    ge_validering = create_knada_nb_pod_operator(dag=dag,
                                                 name="ge-validation",
                                                 repo="navikt/nada-dags",
                                                 nb_path="notebooks/Validate.ipynb",
                                                 email="erik.vattekar@nav.no",
                                                 namespace="nada",
                                                 branch="main",
                                                 log_output=True,
                                                 delete_on_finish=False,
                                                 retries=0,
                                                 do_xcom_push=True,
                                                 retry_delay=timedelta(seconds=5))

    send_epost = EmailOperator(dag=dag,
                               task_id="send_valideringsresultater_epost",
                               to='erik.vattekar@nav.no',
                               subject='GE validering',
                               provide_context=True,
                               html_content="<b><h1> {{ task_instance.xcom_pull(task_ids='ge-validering') }} </h1></b>")

    slack_notification = SlackWebhookOperator(
        dag=dag,
        task_id="slack_valideringsresultater",
        webhook_token=os.environ["SLACK_WEBHOOK_TOKEN"],
        message=f"{{ task_instance.xcom_pull(task_ids='ge-validering') }}",
        channel="#kubeflow-cron-alerts",
        link_names=True,
        icon_emoji=":page_with_curl:",
        provide_context=True,
        proxy=os.environ["HTTPS_PROXY"]
    )

    ge_validering >> send_epost >> slack_notification