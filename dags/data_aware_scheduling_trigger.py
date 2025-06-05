from airflow import DAG, Dataset
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator


with DAG('DataverkAirflowPython', start_date=days_ago(1), schedule=[Dataset("gs://local-flyte-test/file.txt")], catchup=False) as dag:
    trigger_from_data_aware_scheduling = python_operator(
        dag=dag,
        name="data-aware-scheduling-trigger",
        repo="navikt/nada-dags",
        branch="dev",
        script_path="notebooks/read_from_bucket.py",
        requirements_path="notebooks/requirements_write_to_bucket.txt",
        retries=0,
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
    )
