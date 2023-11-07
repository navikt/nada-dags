from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dataverk_airflow import quarto_operator


with DAG('Quarto', start_date=days_ago(1), schedule=None) as dag:
    quarto_op = quarto_operator(
        dag=dag,
        name="quarto-op",
        repo="navikt/nada-dags",
        quarto={
            "path": "notebooks/quarto.ipynb",
            "env": "prod",
            "id": "4bdcde31-5a0d-4e90-8335-8d6b8134deb1",
            "token": Variable.get("TEAM_TOKEN"),
        },
        requirements_path="notebooks/requirements.txt",
    )
