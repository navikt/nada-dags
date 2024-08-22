import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from kubernetes import client as k8s
from airflow.models import Variable
import sqlalchemy
import oracledb
from datetime import datetime
from airflow.providers.slack.notifications.slack import send_slack_notification


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
                channel="#nada-alerts",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ]
    )
    def myfunc(user: str, passw: str):
        engine = sqlalchemy.create_engine(f"oracle+oracledb://{user}:{passw}@dmv07-scan.adeo.no:1521/?service_name=dwhu1")
        with engine.connect() as con:
            con.execute(sqlalchemy.text("drop table testtabell"))
            con.execute(sqlalchemy.text("create table testtabell (value number not null, column2 varchar2(10))"))
            con.execute("insert into testtabell (value,column2) VALUES (1, 'test')")
            con.execute("commit")
            res = con.execute(sqlalchemy.text("SELECT count(*) FROM testtabell"))

            for row in res:
                print(row)

    db_user = Variable.get('db_user')
    db_pass = Variable.get('db_pass')
    myfunc(db_user, db_pass)
