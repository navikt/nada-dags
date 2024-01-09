from airflow.models import DAG, Variable
from airflow.utils.dates import datetime
from dataverk_airflow import notebook_operator
from airflow.decorators import task
from kubernetes import client
from operators.slack_operator import slack_info


with DAG(
  dag_id = 'kopier_BS_data_fra_BigQuery_til_Oracle',
  description = 'kopierer brillestonad data fra en tabell i BigQuery til en tabell i Oracle database',
  start_date=datetime(2023, 2, 21),
  schedule_interval= '@daily',
  max_active_runs=1,
  catchup = False
) as dag:

    @task
    def notification_start():
        slack_info(
            message = f"starttest",
            channel="#kubeflow-cron-alerts"
        )

    start_alert = notification_start()

    bs_data_kopiering = notebook_operator(
    dag = dag,
    name="nb-op",
    repo="navikt/nada-dags",
    nb_path="notebooks/mynb.ipynb",
    allowlist=['dm09-scan.adeo.no:1521', 'slack.com', 'hooks.slack.com'],
    delete_on_finish= False,
    resources=client.V1ResourceRequirements(
        requests={'memory': '4G'},
        limits={'memory': '4G'}),
    slack_channel = "#kubeflow-cron-alerts",
    image='ghcr.io/navikt/dvh_familie_image:2023-11-27-eccc5e8-main',
    log_output=False
    )

    @task
    def notification_end():
        slack_info(
            message = f"endtest",
            channel="#kubeflow-cron-alerts"
        )
    slutt_alert = notification_end()

start_alert >> bs_data_kopiering >> slutt_alert


