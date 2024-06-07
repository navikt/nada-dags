from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dataverk_airflow import quarto_operator


with DAG('DataverkAirflowQuartoSingleFile', start_date=days_ago(1), schedule="5 9 * * 1-5", catchup=False) as dag:
    quarto_op = quarto_operator(
        dag=dag,
        name="quarto-op",
        repo="navikt/nada-dags",
        quarto={
            "path": "notebooks/quarto.ipynb",
            "env": "dev",
            "id": "{{ var.value.get('QUARTO_ID') }}",
            "token": Variable.get("TEAM_TOKEN"),
        },
        requirements_path="notebooks/requirements.txt",
        slack_channel="#nada-alerts",
    )
