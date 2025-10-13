import os
from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dataverk_airflow import quarto_operator


dmp_host = Variable.get('MARKEDSPLASSEN_HOST_DEV', default_var=None)
if dmp_host:
    os.environ["MARKEDSPLASSEN_HOST"] = dmp_host


with DAG('DataverkAirflowQuartoBook', start_date=days_ago(1), schedule="15 8 * * 1-5", catchup=False) as dag:
    quarto_op = quarto_operator(
        dag=dag,
        name="quarto-op",
        repo="navikt/nada-dags",
        python_version="3.10",
        image="europe-north1-docker.pkg.dev/knada-gcp/knada-north/dv-airflow:128",
        use_uv_pip_install=True,
        quarto={
            "folder": "notebooks/quartobook",
            "env": "dev",
            "id": "757da08e-031e-4fac-a5f0-fffe6d2d96b6",
            "token": Variable.get("NADA_TOKEN_DEV"),
        },
        requirements_path="notebooks/requirements.txt",
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
    )
