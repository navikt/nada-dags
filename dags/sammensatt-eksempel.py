from airflow import DAG
from datetime import datetime

from airflow.operators.email_operator import EmailOperator
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('sammensatt-eksempel', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:
    pretask1 = create_knada_nb_pod_operator(dag=dag,
                                            name="knada-pod-operator",
                                            repo="navikt/nada-dags",
                                            nb_path="notebooks/PreTransformationTask1.ipynb",
                                            email="erik.vattekar@nav.no",
                                            slack_channel="#kubeflow-cron-alerts",
                                            namespace="nada",
                                            branch="main",
                                            log_output=False)

    pretask2 = create_knada_nb_pod_operator(dag=dag,
                                            name="knada-pod-operator",
                                            repo="navikt/nada-dags",
                                            nb_path="notebooks/PreTransformationTask1.ipynb",
                                            email="erik.vattekar@nav.no",
                                            slack_channel="#kubeflow-cron-alerts",
                                            namespace="nada",
                                            branch="main",
                                            log_output=False)

    transformation = create_knada_nb_pod_operator(dag=dag,
                                                  name="knada-pod-operator",
                                                  repo="navikt/nada-dags",
                                                  nb_path="notebooks/Transformation.ipynb",
                                                  email="erik.vattekar@nav.no",
                                                  slack_channel="#kubeflow-cron-alerts",
                                                  namespace="nada",
                                                  branch="main",
                                                  log_output=False)

    posttask = create_knada_nb_pod_operator(dag=dag,
                                            name="knada-pod-operator",
                                            repo="navikt/nada-dags",
                                            nb_path="notebooks/PostTransformationTask.ipynb",
                                            email="erik.vattekar@nav.no",
                                            slack_channel="#kubeflow-cron-alerts",
                                            namespace="nada",
                                            branch="main",
                                            log_output=False)

    email_notification = EmailOperator(
        dag=dag,
        task_id="success-notification",
        to='erik.vattekar@nav.no',
        subject='Great success!',
        html_content='<p> Airflow dag succeeded <p>')

    [pretask1, pretask2] >> transformation >> posttask >> email_notification
