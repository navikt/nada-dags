from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator
from airflow.models import Variable


oracle_user = Variable.get('ORACLE_DB_USER')
oracle_pass = Variable.get('ORACLE_DB_PASSWORD')
oracle_host = Variable.get('ORACLE_DB_HOST')
oracle_port = Variable.get('ORACLE_DB_PORT')
oracle_table_name = Variable.get('ORACLE_DB_TABLE_NAME')
oracle_service_name = Variable.get('ORACLE_DB_SERVICE_NAME')


with DAG('DataverkAirflowPythonOracleClient', start_date=days_ago(1), schedule="20 13 * * 1-5", catchup=False) as dag:
    py_op = python_operator(
        dag=dag,
        name="python-op-oracle-client-uv",
        repo="navikt/nada-dags",
        script_path="notebooks/connectorx-script.py",
        requirements_path="notebooks/requirements-connectorx.txt",
        allowlist=["dmv04-scan.adeo.no:1521"],
        extra_envs={
            "ORACLE_DB_USER": oracle_user,
            "ORACLE_DB_PASSWORD": oracle_pass,
            "ORACLE_DB_HOST": oracle_host,
            "ORACLE_DB_PORT": oracle_port,
            "ORACLE_DB_TABLE_NAME": oracle_table_name,
            "ORACLE_DB_SERVICE_NAME": oracle_service_name,
        },
        retries=0,
        #slack_channel="#nada-alerts-dev",
        use_uv_pip_install=True,
    )
