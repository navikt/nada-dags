from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from kubernetes import client as k8s
from kode.modul import mycallable

MOUNT_PATH = "/code"
REPO = "navikt/nada-airflow"
BRANCH = "main"

def temp():
    import time
    print("start")
    time.sleep(1000)

with DAG('python-operator-with-extra-initcontainer', start_date=days_ago(1), schedule_interval=None) as dag:    
    run_this = PythonOperator(
    task_id='test-pythonoperator',
    python_callable=temp,
    executor_config={
        "pod_override": k8s.V1Pod(
            spec=k8s.V1PodSpec(
                init_containers=[
                    k8s.V1Container(
                        name="clone-code-repo",
                        image="europe-west1-docker.pkg.dev/knada-gcp/knada/git-sync:2023-03-09-bfc0f3e",
                        command=["/bin/sh", "-c"],
                        args=[f"/git-clone.sh {REPO} {BRANCH} {MOUNT_PATH}"],
                        volume_mounts=[
                            k8s.V1VolumeMount(
                                name="code", mount_path=MOUNT_PATH, sub_path=None, read_only=False
                            ),
                            k8s.V1VolumeMount(
                                name="airflow-git-secret",
                                mount_path="/keys",
                                sub_path=None,
                                read_only=False,
                            ),
                        ],
                    )
                ],
            ),
                containers=[
                    k8s.V1Container(
                       name="base",
                       image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-papermill:2023-03-22-fb1c4a4"
                    )
                ],
                volumes= [
                    k8s.V1Volume(
                        name="code"
                    )
                ]
            )
    },
    dag=dag)
