from datetime import timedelta, datetime
import pendulum

from airflow import DAG

from dataverk_airflow.knada_operators import create_knada_nb_pod_operator

europe = pendulum.timezone("Europe/Oslo")

with DAG(
        'dialoger',
        start_date=datetime(year=2021, month=11, day=17, hour=20, minute=15, tzinfo=europe),
        schedule_interval=None,
        max_active_runs=1,
        catchup=False,
        dagrun_timeout=timedelta(hours=3)
) as dag:
    navn = create_knada_nb_pod_operator(dag=dag,
                                        slack_channel="#kubeflow-cron-alerts",
                                        name="navn",
                                        repo="navikt/nada-dags",
                                        nb_path="notebooks/mynb.ipynb",
                                        branch="main",
                                        image = 'ghcr.io/navikt/knada-images/test-image:v2',
                                        delete_on_finish=False,
                                        log_output=False)
