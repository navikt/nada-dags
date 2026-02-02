from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator
from kubernetes import client


with DAG('DataverkAirflowPython', start_date=days_ago(1), schedule="10 8 * * 1-5", catchup=False) as dag:
    py_op = python_operator(
        dag=dag,
        name="python-op",
        repo="navikt/nada-dags",
        script_path="notebooks/script.py",
        requirements_path="notebooks/requirements.txt",
        retries=0,
        do_xcom_push=True,
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
        client.V1ResourceRequirements(
            requests={"memory": "1G", "cpu": "5",},
            limits={"memory": "1G"}
        )
    )
