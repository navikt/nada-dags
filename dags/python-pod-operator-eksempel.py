from airflow import DAG
from datetime import datetime, timedelta
from dataverk_airflow.knada_operators import create_knada_python_pod_operator


with DAG('knada-python-pod-operator-eksempel', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:
    task = create_knada_python_pod_operator(dag=dag,
                                            name="knada-python-pod-operator",
                                            repo="navikt/nada-dags",
                                            script_path="scripts/main.py",
                                            email="erik.vattekar@nav.no",
                                            namespace="nada",
                                            branch="main",
                                            retries=1,
                                            delete_on_finish=False,
                                            retry_delay=timedelta(seconds=5))
