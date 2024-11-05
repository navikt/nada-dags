from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator


# For å konfigurere tilgang for airflow service account, se https://docs.knada.io/analyse/eksempler/#cloud-sql-iam-database-authentication
with DAG('CloudSQLPostgres', start_date=days_ago(1), schedule="50 8 * * 1-5", catchup=False) as dag:
    postgres_op = python_operator(
        dag=dag,
        name="postgres-op",
        repo="navikt/nada-dags",
        script_path="notebooks/read_postgres.py",
        requirements_path="notebooks/requirements_pg.txt",
        allowlist=["34.88.107.185:3307","34.88.107.185:443"],
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
        extra_envs={
            "CLOUDSQL_DB_IAM_USER": "{{ var.value.get('CLOUDSQL_DB_IAM_USER') }}"
        }
        retries=0,
    )
