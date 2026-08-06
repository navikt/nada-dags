from airflow import DAG
from airflow.decorators import task
import pendulum
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from kubernetes import client as k8s
from airflow.models import Variable

oracle_user = Variable.get('ORACLE_DB_USER')
oracle_pass = Variable.get('ORACLE_DB_PASSWORD')
oracle_host = Variable.get('ORACLE_DB_HOST')
oracle_port = Variable.get('ORACLE_DB_PORT')
oracle_table_name = Variable.get('ORACLE_DB_TABLE_NAME')
oracle_service_name = Variable.get('ORACLE_DB_SERVICE_NAME')

def read_oracle():
  import pandas as pd
  import sqlalchemy
  import oracledb
  oracledb.version = "8.3.0"
  import sys
  sys.modules["cx_Oracle"] = oracledb

  engine = sqlalchemy.create_engine(f"oracle://{oracle_user}:{oracle_pass}@{oracle_host}:{oracle_port}/?service_name={oracle_service_name}")
  db_conn = engine.connect()
  db_source= pd.read_sql_query(sqlalchemy.text(f"SELECT * FROM {oracle_table_name}"),con=db_conn)

  print(db_source.head())  
  

with DAG(
    'python-operator-read-oracle', 
    schedule_interval = '15 0 * * *', 
    start_date= datetime(2022, 9, 1, tzinfo=pendulum.timezone("Europe/Oslo")),
    catchup = False, 
    tags =["syfo_kandidakter_enhet", "slack", "oracle", "postgres"],
    max_active_runs=1,
) as dag:
  t_kandidat_enhet_lasting_1  = PythonOperator(
    dag=dag,
    task_id='read_oracle', 
    python_callable=read_oracle,
    executor_config={
        "pod_override": k8s.V1Pod(
          metadata=k8s.V1ObjectMeta(annotations={"allowlist": ",".join([f"{oracle_host}:{oracle_port}"])}) 
        )
    },
  )