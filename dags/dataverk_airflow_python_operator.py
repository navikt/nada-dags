from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator


with DAG('DataverkAirflowPython', start_date=days_ago(1), schedule="10 8 * * 1-5", catchup=False) as dag:
    py_op = python_operator(
        dag=dag,
        name="python-op",
        repo="navikt/nada-dags",
        script_path="notebooks/script.py",
        requirements_path="notebooks/requirements.txt",
        slack_channel="#kubeflow-cron-alerts",
        retries=0,
        do_xcom_push=True,
    )
