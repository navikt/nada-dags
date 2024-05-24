import os
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s

with DAG('KubernetesPodOperator', start_date=datetime(2023, 2, 15), schedule=None) as dag:

    k8s_pod_op = KubernetesPodOperator(
        image=os.getenv("KNADA_AIRFLOW_OPERATOR_IMAGE"),
        annotations={"allowlist": ""},
        cmds=["/bin/sh", "-c"],
        arguments=['echo "hello world"'],
        name="k8s_pod_operator",
        task_id="k8s-pod-operator",
        env_vars={"name": "value"},
        image_pull_secrets=[k8s.V1LocalObjectReference('ghcr-secret')],
        is_delete_operator_pod=True,
        get_logs=True,
        labels={
            "component": "worker",
            "release": "airflow"
        },
        full_pod_spec=k8s.V1Pod(
            spec=k8s.V1PodSpec(
                containers=[
                    k8s.V1Container(
                        name="base",
                        working_dir="/workspace"
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
