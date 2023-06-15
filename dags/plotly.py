from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from kubernetes import client as k8s
import os

#from mymodule.mymodule import my_funky_func


def mycallable():
    import plotly
    print("hello")



with DAG('plotly', start_date=days_ago(1), schedule_interval=None) as dag:    
    run_this = PythonOperator(
    task_id='test-plotly',
    python_callable=mycallable,
    executor_config={
        "pod_override": k8s.V1Pod(
            spec=k8s.V1PodSpec(
                containers=[
                   k8s.V1Container(
                      name="base",
                      image="ghcr.io/navikt/airflow-pensjon-sb:v0"
                   )
                ]
            )
        )
    },
    dag=dag)
