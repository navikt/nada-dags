from airflow import DAG
from datetime import datetime, timedelta
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('ge-validation', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:
    task = create_knada_nb_pod_operator(dag=dag,
                                        name="ge-validation",
                                        repo="navikt/bq-dags",
                                        nb_path="validate/Validate.ipynb",
                                        email="erik.vattekar@nav.no",
                                        namespace="nada",
                                        branch="main",
                                        log_output=True,
                                        retries=0,
                                        retry_delay=timedelta(seconds=5))
