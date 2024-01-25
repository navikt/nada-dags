from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dataverk_airflow import quarto_operator


with DAG('QuartoBook', start_date=days_ago(1), schedule=None) as dag:
    quarto_op = quarto_operator(
        dag=dag,
        name="quarto-op",
        repo="navikt/nada-dags",
        image="europe-north1-docker.pkg.dev/knada-gcp/knada-north/dataverk-airflow-python-3.8",
        quarto={
            "folder": "notebooks/quartobook",
            "env": "dev",
            "id": "757da08e-031e-4fac-a5f0-fffe6d2d96b6",
            "token": Variable.get("NADA_TOKEN_DEV"),
        },
        requirements_path="notebooks/requirements.txt",
    )
