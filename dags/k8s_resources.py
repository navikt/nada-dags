from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as client

task = KubernetesPodOperator(
    cmds=["bash", "-cx"],
    arguments=["echo", "10", "echo pwd"],
    name="k8s_resource_example",
    task_id="task-one",
    get_logs=True,
    container_resources=client.V1ResourceRequirements(
        requests={"ephemeral-storage": "2Gi"}
    ),
)

task >> run_this
