from airflow import DAG
from datetime import datetime, timedelta
from dataverk_airflow.knada_operators import create_knada_python_pod_operator


with DAG('dp-test', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:
    task = create_knada_python_pod_operator(dag=dag,
                                            name="dp-test",
                                            repo="navikt/nada-dags",
                                            script_path="scripts/dp.py",
                                            email="erik.vattekar@nav.no",
                                            namespace="nada",
                                            branch="main",
                                            delete_on_finish=False,
                                            retries=1,
                                            retry_delay=timedelta(seconds=5))
