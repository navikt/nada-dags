from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import notebook_operator


with DAG('Notebook', start_date=days_ago(1), schedule=None) as dag:
    nb_op = notebook_operator(
        dag=dag,
        name="nb-op",
        repo="navikt/nada-dags",
        nb_path="notebooks/mynb.ipynb",
        requirements_path="notebooks/requirements.txt",
    )
