import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from kubernetes import client as k8s
from airflow.models import Variable
import sqlalchemy
import oracledb
import sys
from datetime import datetime
from airflow.providers.slack.notifications.slack import send_slack_notification
oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb


with DAG('DecoratorExampleWithPodOverrideReadOnpremOracle', start_date=datetime(2023, 2, 14), schedule="20 8 * * 1-5", catchup=False) as dag:
    @task(
        executor_config = {
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "dmv07-scan.adeo.no:1521,hooks.slack.com"})
            )
        },
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of dag {{ dag }} failed",
                channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ]
    )
    def myfunc(user: str, passw: str, host: str, port: int, service_name: str):
        engine = sqlalchemy.create_engine(f"oracle://{user}:{passw}@{host}:{port}/?service_name={service_name}")
        with engine.connect() as con:
            con.execute(sqlalchemy.text("drop table testtabell"))
            con.execute(sqlalchemy.text("create table testtabell (value number not null, column2 varchar2(10))"))
            con.execute("insert into testtabell (value,column2) VALUES (1, 'test')")
            con.execute("commit")
            res = con.execute(sqlalchemy.text("SELECT count(*) FROM testtabell"))

            for row in res:
                print(row)

    db_user = Variable.get('ORACLE_DB_USER')
    db_pass = Variable.get('ORACLE_DB_PASSWORD')
    host = Variable.get('ORACLE_DB_HOST')
    port = Variable.get('ORACLE_DB_PORT')
    service_name = Variable.get('ORACLE_DB_SERVICE_NAME')
    myfunc(db_user, db_pass, host, port, service_name)
