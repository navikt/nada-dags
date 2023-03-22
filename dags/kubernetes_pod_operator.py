from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as client

with DAG('KubernetesPodOperator', start_date=datetime(2023, 2, 15)) as dag:

    task_1 = KubernetesPodOperator(
        image="bash:latest",
        cmds=["bash", "-cx"],
        arguments=["echo", "10", "echo pwd"],
        name="k8s_resource_example",
        task_id="task-one",
        get_logs=True,
        container_resources=client.V1ResourceRequirements(
            requests={
                "ephemeral-storage": "2Gi"
            }
        ),
        annotations={"allowlist": "https://g.nav.no"},
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
            k8s.V1Volume(
                name="airflow-git-secret",
                secret=k8s.V1SecretVolumeSource(
                    default_mode=448,
                    secret_name="github-app-secret",
                ),
            ),
        ],
        init_containers=[
            k8s.V1Container(
                name="clone-repo",
                image="europe-west1-docker.pkg.dev/knada-gcp/knada/git-sync:2023-03-08-80342e3",
                volume_mounts=[
                    k8s.V1VolumeMount(
                        name="dags-data",
                        mount_path="/dags",
                        sub_path=None,
                        read_only=False
                    ),
                    k8s.V1VolumeMount(
                        name="airflow-git-secret",
                        mount_path="/keys",
                        sub_path=None,
                        read_only=False,
                    ),
                ],
                command=["/bin/sh", "-c"],
                args=["/git-clone.sh navikt/nada-dags main /dags"],
            )
        ]
    )