from airflow import DAG
from datetime import datetime
from kubernetes.client import models as k8s
from airflow.models import Variable
from dataverk_airflow import notebook_operator, python_operator, quarto_operator


with DAG('NewDataverkAirflow', start_date=datetime(2023, 2, 15), schedule=None) as dag:
    nb_op = notebook_operator(
        dag = dag,
        name = "nb-op",
        repo = "navikt/nada-dags",
        nb_path = "notebooks/mynb.ipynb",
        requirements_path="notebooks/requirements.txt",
    )

    py_op = python_operator(
        dag = dag,
        name = "python-op",
        repo = "navikt/nada-dags",
        script_path = "notebooks/script.py",
        requirements_path="notebooks/requirements.txt",
    )

    quarto_op = quarto_operator(
        dag=dag,
        name="quarto-op",
        repo="navikt/nada-dags",
        quarto={
            "path": "notebooks/quarto.ipynb",
            "env": "prod",
            "id": "4bdcde31-5a0d-4e90-8335-8d6b8134deb1",
            "token": Variable.get("quarto_token"),
        },
        requirements_path="notebooks/requirements.txt",
    )

    nb_op
    py_op
    quarto_op
