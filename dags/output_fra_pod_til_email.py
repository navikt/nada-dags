from datetime import timedelta
from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('output-fra-pod-til-epost-operatah', start_date=days_ago(1), schedule_interval="0 14 * * *") as dag:
    output_fra_pod = create_knada_nb_pod_operator(dag=dag,
                                                  name="pod-som-lager-output",
                                                  repo="navikt/nada-dags",
                                                  nb_path="notebooks/OutputFromPodOperator.ipynb",
                                                  email="erik.vattekar@nav.no",
                                                  namespace="nada",
                                                  branch="main",
                                                  log_output=False,
                                                  retries=3,
                                                  retry_delay=timedelta(seconds=5))

    send_epost = EmailOperator(dag=dag,
                               task_id="send_email",
                               to='erik.vattekar@nav.no',
                               subject='Test mail',
                               provide_context=True,
                               html_content="<b><h1> {{ task_instance.xcom_pull(task_ids='pod-som-lager-output') }} </h1></b>")

    output_fra_pod >> send_epost
