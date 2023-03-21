from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from datetime import datetime
from airflow.utils.dates import days_ago
from kubernetes import client as k8s


with DAG('bash-operator-notebook', start_date=days_ago(1), schedule_interval=None, catchup=False) as dag:

    t1 = KubernetesPodOperator(
        task_id='notebook',
        cmds=["bash", "-c"],
        arguments=["papermill", "--log-output", "/dags/notebooks/mynb.ipynb", "/dags/output.ipynb"],
        image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-notebooks:2023-03-08-d3684b7",
        dag=dag
    )
