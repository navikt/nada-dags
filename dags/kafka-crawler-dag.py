from airflow import DAG
from airflow.kubernetes.volume import Volume
from airflow.kubernetes.volume_mount import VolumeMount
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta
import kubernetes.client as k8s

default_args = {
    'start_date': datetime(2020, 10, 28)
}

envs = [k8s.V1EnvVar(name='HTTPS_PROXY', value='http://webproxy.nais:8088'),
        k8s.V1EnvVar(name='https_proxy', value='http://webproxy.nais:8088')]

git_clone_init_container = k8s.V1Container(
            name="init-clone-repo",
            image="navikt/knada-git-sync:9",
            volume_mounts=[
                k8s.V1VolumeMount(name="dags-data", mount_path="/dags", sub_path=None, read_only=False),
                k8s.V1VolumeMount(name="git-clone-secret", mount_path="/keys", sub_path=None, read_only=False)
            ],
            env=envs,
            command=["/bin/sh", "/git-clone.sh"],
            args=["navikt/nada-dags", "main", "/dags"]
        )

with DAG('kafka-indexer', default_args=default_args, schedule_interval=None) as dag:
    t1 = BashOperator(
        task_id='testinit',
        bash_command='echo "test"',
        dag=dag)
    t2 = KubernetesPodOperator(
        init_containers=[git_clone_init_container],
        dag=dag,
        name='kafka-indexer',
        namespace='nada',
        task_id='kafka-indexer',
        image='navikt/knada-airflow-nb:5',
        env_vars={
            "LOG_ENABLED": "false",
            "NOTEBOOK_NAME": "/dags/notebooks/kafka/kafka_crawler.ipynb"
        },
        volume_mounts=[
            VolumeMount(name="dags-data", mount_path="/dags", sub_path=None, read_only=True)
        ],
        volumes=[
            Volume(name='dags-data', configs={}),
            Volume(name="git-clone-secret", configs={
                "secret": {
                    "defaultMode": 448,
                    "secretName": "airflow-git-keys"
                }
            })
        ],
        annotations={
            "sidecar.istio.io/inject": "false"
        }
    )

    t1 >> t2
