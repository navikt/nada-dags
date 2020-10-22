from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from datetime import datetime, timedelta


default_args = {
    'start_date': datetime(2020, 10, 21)
}

with DAG('kafka-indexer', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    t1 = BashOperator(
        task_id='testinit',
        bash_command='echo "test"',
        dag=dag)
    t2 = KubernetesPodOperator(
        dag=dag,
        name='kafka-indexer',
        namespace='nada',
        task_id='kafka-indexer',
        image='navikt/knada-airflow-nb:4',
        env_vars={
            "LOG_ENABLED": "false",
            "NOTEBOOK_NAME": "/dags/notebooks/kafka/kafka_crawler.ipynb"
        },
        volume_mounts=[
            VolumeMount("dags-data", mount_path="/dags", sub_path=None, read_only=True)
        ],
        volumes=[
            Volume(name='dags-data', configs={})
        ],
        annotations={
            "sidecar.istio.io/inject": "false"
        }
    )

    t1 >> t2
