import pendulum
from kubernetes.client import models as k8s
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.slack.notifications.slack import send_slack_notification

default_args = {
    'owner': 'airflow'
}

with DAG(
        dag_id='LargePodRequest',
        default_args=default_args,
        schedule="35 8 * * 1-5", 
        catchup=False,
        is_paused_upon_creation=True,
        start_date=pendulum.today('UTC').add(days=-2),
        max_active_runs=1,
        tags=['k8s-pod-operator', 'huge-task'],
) as dag:
    k = KubernetesPodOperator(
        image="ubuntu:noble-20240429",
        cmds=["bash", "-cx"],
        arguments=["echo hello"],
        annotations={"allowlist": "hooks.slack.com"},
        name="k8s-pod",
        task_id="huge-pod",
        hostnetwork=False,
        get_logs=True,
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
        startup_timeout_seconds=1000,
        labels={
            "component": "worker",
            "release": "airflow"
        },
        container_resources=k8s.V1ResourceRequirements(
            requests={
                "memory": "256Gi",
                "ephemeral-storage": "128Mi",
                "cpu": "10"
            }
        ),
        security_context=k8s.V1PodSecurityContext(
            fs_group=0,
            seccomp_profile=k8s.V1SeccompProfile(
                type="RuntimeDefault"
            )
        ),
        node_selector={
            "workload": "resource_intensive"
        },
        tolerations=[
            k8s.V1Toleration(
                key="dedicated",
                operator="Equal",
                value="resource_intensive",
                effect="NoSchedule"
            )
        ]
    )
