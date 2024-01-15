from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator


with DAG('CloudSQLPostgres', start_date=days_ago(1), schedule=None) as dag:
    postgres_op = python_operator(
        dag=dag,
        name="postgres-op",
        repo="navikt/nada-dags",
        script_path="notebooks/read_postgres.py",
        requirements_path="notebooks/requirements_pg.txt",
        allowlist=["34.88.183.183:3307","34.88.183.183:443"],
    )
