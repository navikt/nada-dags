import os
from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dataverk_airflow import quarto_operator


dmp_host = Variable.get('MARKEDSPLASSEN_HOST_DEV', default_var=None)
if dmp_host:
    os.environ["MARKEDSPLASSEN_HOST"] = dmp_host


with DAG('DataverkAirflowQuartoSingleFile', start_date=days_ago(1), schedule="5 9 * * 1-5", catchup=False) as dag:
    quarto_op = quarto_operator(
        dag=dag,
        name="quarto-op",
        repo="navikt/nada-dags",
        quarto={
            "path": "notebooks/quarto.ipynb",
            "env": "dev",
            "id": "f6f86316-9301-4ac3-a43b-46d238520cda",
            "token": Variable.get("NADA_TOKEN_DEV"),
        },
        use_uv_pip_install=True,
        requirements_path="notebooks/requirements.txt",
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
    )
