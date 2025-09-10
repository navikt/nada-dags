from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import kubernetes_operator


with DAG('DataverkAirflowPythonEntrypointOverride', start_date=days_ago(1), schedule="10 13 * * 1-5", catchup=False) as dag:
    py_op = kubernetes_operator(
        dag=dag,
        name="dataverk-airflow-entrypoint-override",
        repo="navikt/nada-dags",
        image="europe-north1-docker.pkg.dev/knada-gcp/knada-north/dataverk-airflow-python-3.11-man:v127",
        entrypoint=[
            "dbt",
            "run",
        ],
        retries=0,
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
    )
