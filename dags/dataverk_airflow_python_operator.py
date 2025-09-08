from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator


with DAG('DataverkAirflowPython', start_date=days_ago(1), schedule="10 8 * * 1-5", catchup=False) as dag:
    py_op = python_operator(
        dag=dag,
        name="python-op",
        repo="navikt/nada-dags",
        script_path="notebooks/script.py",
        image="europe-north1-docker.pkg.dev/knada-gcp/knada-north/dataverk-airflow-python-3.12-man:v2",
        requirements_path="notebooks/requirements.txt",
        retries=0,
        do_xcom_push=True,
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
    )
