import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from kubernetes import client as k8s


with DAG('DecoratorExampleWithPodOverride', start_date=datetime(2023, 2, 14), schedule=None) as dag:
    @task(
        executor_config = {
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": "slack.com"})
            )
        }
    )
    def myfunc(value: str):
        print(value)

    myfunc("hello")