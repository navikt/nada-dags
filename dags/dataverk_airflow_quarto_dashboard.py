import os
from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dataverk_airflow import quarto_operator


dmp_host = Variable.get('MARKEDSPLASSEN_HOST_DEV', default_var=None)
if dmp_host:
    os.environ["MARKEDSPLASSEN_HOST"] = dmp_host


with DAG('DataverkAirflowQuartoDashboard', start_date=days_ago(1), schedule="5 12 * * 1-5", catchup=False) as dag:
    quarto_op = quarto_operator(
        dag=dag,
        name="quarto-op",
        repo="navikt/nada-dags",
        image="europe-north1-docker.pkg.dev/knada-gcp/knada-north/dataverk-airflow-python-3.12-man:v2",
        quarto={
            "folder": "notebooks/quarto",
            "env": "dev",
            "id": "f87e918a-e5bb-4549-aba2-78ebc6c6ae2c",
            "token": Variable.get("NADA_TOKEN_DEV"),
        },
        requirements_path="notebooks/requirements.txt",
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
    )
