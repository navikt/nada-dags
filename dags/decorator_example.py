import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from kubernetes import client as k8s
import cx_Oracle as cx
from airflow.models import Variable
import sqlalchemy
from datetime import datetime


with DAG('DecoratorExampleWithPodOverride', start_date=datetime(2023, 2, 14), schedule=None) as dag:
    @task(
        executor_config = {
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "dm07-scan.adeo.no:1521"})
            )
        }
    )
    def myfunc(user: str, passw: str):
        engine = sqlalchemy.create_engine(f"oracle://{user}:{passw}@dm07-scan.adeo.no:1521/?service_name=dwhu1")
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
