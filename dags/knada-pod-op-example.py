from airflow import DAG
from datetime import datetime
import pendulum
from dataverk_airflow.knada_operators import create_knada_python_pod_operator

with DAG(
    dag_id="pod operator",
    description="dette er en pod operator",
    schedule_interval=None,
    start_date=datetime(2023, 1, 26, tzinfo=pendulum.timezone("Europe/Oslo")),
    catchup=False,
) as dag:
  podop = create_knada_python_operator(
              dag=dag, 
              name="task",
              repo="navikt/nada-dags",
              branch="main",
              script_path="notebooks/script.py",
              image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow:2023-03-22-ffd1ef0"
  )
