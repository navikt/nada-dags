import os
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s
from airflow.providers.slack.notifications.slack import send_slack_notification

with DAG('KubernetesPodOperator', start_date=datetime(2023, 2, 15), schedule="40 8 * * 1-5", catchup=False) as dag:

    k8s_pod_op = KubernetesPodOperator(
        image=os.getenv("KNADA_AIRFLOW_OPERATOR_IMAGE"),
        annotations={"allowlist": "g.nav.no"},
        startup_timeout_seconds=720,
        cmds=["/bin/sh", "-c"],
        arguments=['echo "hello world"; curl https://g.nav.no'],
        name="k8s_pod_operator",
        is_delete_operator_pod=True,
        task_id="k8s-pod-operator",
        env_vars={"name": "value"},
        on_failure_callback=[
            send_slack_notification(
                text="{{ task }} run {{ run_id }} of {{ dag }} failed",
                channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
                slack_conn_id="slack_connection",
                username="Airflow",
            )
        ],
        image_pull_secrets=[k8s.V1LocalObjectReference('ghcr-secret')],
        get_logs=True,
        labels={
            "component": "worker",
            "release": "airflow"
        },
        full_pod_spec=k8s.V1Pod(
            metadata=k8s.V1ObjectMeta(annotations={"allowlist": "hooks.slack.com"}),
            spec=k8s.V1PodSpec(
                containers=[
                    k8s.V1Container(
                        name="base",
                        working_dir="/workspace",
                        security_context=k8s.V1SecurityContext(
                            allow_privilege_escalation=False,
                            run_as_user=50000,
                        )
                    )
                ]
            )
        ),
        container_resources=k8s.V1ResourceRequirements(
            requests={
                "memory": "2Gi",
                "ephemeral-storage": "128Mi",
                "cpu": "2"
            }
        ),
        volume_mounts=[
            k8s.V1VolumeMount(
                name="dags-data",
                mount_path="/dags",
                sub_path=None,
                read_only=False
            ),
            k8s.V1VolumeMount(
                name="ca-bundle-pem",
                mount_path="/etc/pki/tls/certs/ca-bundle.crt",
                read_only=True,
                sub_path="ca-bundle.pem"
            ),
        ],
        volumes=[
            k8s.V1Volume(
                name="dags-data"
            ),
            k8s.V1Volume(
                name="ca-bundle-pem",
                config_map=k8s.V1ConfigMapVolumeSource(
                    default_mode=420,
                    name="ca-bundle-pem",
                )
            ),
        ],
        security_context=k8s.V1PodSecurityContext(
            fs_group=0,
            run_as_non_root=True,
            seccomp_profile=k8s.V1SeccompProfile(
                type="RuntimeDefault"
            )
        ),
    )
