from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator
from kubernetes import client as k8s
import os
import logging
import time

def myfunc():
    import requests
    logging.info("func")
    logging.warning(f"team secret path {os.environ['KNADA_TEAM_SECRET']}")
    #time.sleep(120)
    res = requests.get("https://ssb.no/api")
    res.raise_for_status()
    print(res.status_code)

with DAG('test-k8s-exec', start_date=days_ago(1), schedule_interval=None) as dag:
    #slack = SlackWebhookOperator(
    #http_conn_id=None,
    #task_id="slack-message",
    #webhook_token=os.environ["SLACK_TOKEN"],
    #message="asdf",
    #channel="#kubeflow-cron-alerts",
    #link_names=True,
    #executor_config={
    #    "pod_override": k8s.V1Pod(
    #        metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"})
    #    )
    #}
    #)
    
    #run_this = PythonOperator(
    #task_id='test',
    #python_callable=myfunc,
    #wait_for_downstream=False,
    #provide_context=True,
    #executor_config={
    #    "pod_override": k8s.V1Pod(
    #        metadata=k8s.V1ObjectMeta(annotations={"allowlist": "ssb.no,dm07-scan.adeo.no:1521"}),
    #        spec=k8s.V1PodSpec(
    #            containers=[
    #               k8s.V1Container(
    #                  name="base",
    #                  resources={
    #                    "requests": {
    #                        "cpu": "2"
    #                    }
    #                  }
    #               )
    #            ]
    #        )
    #    )
    #},
    #dag=dag)
    
    then = create_knada_nb_pod_operator(dag=dag,
                                        name="knada-pod-operator",
                                        slack_channel="#kubeflow-cron-alerts",
                                        repo="navikt/nada-dags",
                                        nb_path="notebooks/mynb.ipynb",
                                        retries=1,
                                        delete_on_finish=False,
                                        allowlist=["ssb.no", "dm07-scan.adeo.no:1521"],
                                        branch="main")
    
    #then_this = KubernetesPodOperator(
    #    dag=dag,
    #    name="tasken",
    #    task_id="tasken",
    #    cmds=["/bin/bash", "-cx"],
    #    arguments=["echo", "hello"],
    #    executor_config={
    #        "pod_override": k8s.V1Pod(
    #            metadata=k8s.V1ObjectMeta(annotations={"allowlist": "ssb.no,dm07-scan.adeo.no:1521"})
    #        )
    #    }
    #)

    #slack >> run_this >> then #>> then_this
    then
