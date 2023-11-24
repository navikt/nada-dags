from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator


with DAG('PythonTestErrorNotification', start_date=days_ago(1), schedule=None) as dag:
    py_op = python_operator(
        dag=dag,
        name="python-op",
        repo="navikt/nada-dags",
        script_path="notebooks/errorscript.py",
        slack_channel="#kubeflow-cron-alerts",
    )
