from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator
from airflow.providers.slack.notifications.slack import send_slack_notification


# For å konfigurere tilgang for airflow service account, se https://docs.knada.io/analyse/eksempler/#cloud-sql-iam-database-authentication
with DAG('CloudSQLPostgres', start_date=days_ago(1), schedule="50 8 * * 1-5", catchup=False) as dag:
    postgres_op = python_operator(
        dag=dag,
        name="postgres-op",
        repo="navikt/nada-dags",
        script_path="notebooks/read_postgres.py",
        requirements_path="notebooks/requirements_pg.txt",
        allowlist=["34.88.107.185:3307","34.88.107.185:443"],
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel="#nada-alerts-dev",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
    )
