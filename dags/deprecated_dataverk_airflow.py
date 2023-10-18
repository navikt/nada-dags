from airflow import DAG
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator
from airflow.utils.dates import days_ago

with DAG('dag', start_date=days_ago(1), schedule_interval=None) as dag:
    task = create_knada_nb_pod_operator(dag=dag,
                                        name="knada-pod-operator",
                                        repo="navikt/repo",
                                        nb_path="notebooks/mynb.ipynb",
                                        retries=1,
                                        branch="main")
