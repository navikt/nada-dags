from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as client

with DAG('KubernetesPodOperator', start_date=datetime(2023, 2, 15), schedule_interval="@daily") as dag:

    task_1 = KubernetesPodOperator(
        cmds=["bash", "-cx"],
        arguments=["echo", "10", "echo pwd"],
        name="k8s_resource_example",
        task_id="task-one",
        get_logs=True,
        container_resources=client.V1ResourceRequirements(
            requests={"ephemeral-storage": "2Gi"}
        ),
        annotations={"allowlist": "https://g.nav.no"},
    )
