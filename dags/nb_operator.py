from airflow import DAG

from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('test-nb-operator', start_date=days_ago(1), schedule_interval=None) as dag:
    t1 = create_knada_nb_pod_operator(dag=dag,
                                      name="knada-pod-operator",
                                      repo="navikt/nada-dags",
                                      nb_path="notebooks/mynb.ipynb",
                                      branch="main",
                                      delete_on_finish=False,
                                      log_output=True)

    t1
