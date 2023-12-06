from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s

with DAG('KubernetesPodOperator', start_date=datetime(2023, 2, 15), schedule=None) as dag:

    task_1 = KubernetesPodOperator(
        image="ghcr.io/navikt/dvh-kafka-airflow-consumer:0.4.8",
        cmds=["/bin/sh", "-c"],
        arguments=["""python -c "from kafka import KafkaProducer; producer = KafkaProducer(bootstrap_servers='nav-prod-kafka-nav-prod.aivencloud.com:26484', security_protocol='SSL')" """],
        name="k8s_resource_example",
        task_id="task-one",
        env_vars={"name": "value"},
        annotations={"allowlist": "nav-prod-kafka-nav-prod.aivencloud.com:26484"},
        image_pull_secrets=[k8s.V1LocalObjectReference('ghcr-secret')],
        is_delete_operator_pod=False,
        get_logs=True,
        full_pod_spec=k8s.V1Pod(
            spec=k8s.V1PodSpec(
                containers=[
                    k8s.V1Container(
                        name="base",
                        working_dir="/opt"
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
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            working_dir="/opt",
                            env=[
                                k8s.V1EnvVar(name="teste", value="tester")
                            ]
                        )
                    ]
                )
            )
        },
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
        ],
        security_context=k8s.V1PodSecurityContext(
            fs_group=0,
            seccomp_profile=k8s.V1SeccompProfile(
                type="RuntimeDefault"
            )
        ),
    )
