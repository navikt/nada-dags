from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import client as k8s

with DAG('k8s_knaudit_example',
         start_date=datetime(2023, 3, 9)) as dag:
    task_1 = KubernetesPodOperator(
        name="knaudit",
        task_id="task-one",
        get_logs=True,
        image="europe-west1-docker.pkg.dev/knada-gcp/knada/knaudit:2023-03-09-f174567",
        env_vars=[
            k8s.V1EnvFromSource(
                name="ELASTICSEARCH_URL",
                value="https://log-ingest.adeo.no",
            ),
            k8s.V1EnvFromSource(
                name="ELASTICSEARCH_INDEX",
                value="tjenestekall-knada-airflow-run-audit",
            ),
            k8s.V1EnvFromSource(
                name="CA_CERT_PATH",
                value="/etc/pki/tls/certs/ca-bundle.crt",
            ),
            k8s.V1EnvFromSource(
                name="GIT_REPO_PATH",
                value="/dags",
            ),
            k8s.V1EnvFromSource(
                name="AIRFLOW_DAG_ID",
                value_from=k8s.V1EnvFromSource(
                    field_ref=k8s.V1ObjectFieldSelector(
                        field_path="metadata.labels['dag_id']",
                    ),
                ),
            ),
            k8s.V1EnvFromSource(
                name="AIRFLOW_RUN_ID",
                value_from=k8s.V1EnvFromSource(
                    field_ref=k8s.V1ObjectFieldSelector(
                        field_path="metadata.labels['run_id']",
                    ),
                ),
            ),
            k8s.V1EnvFromSource(
                name="AIRFLOW_TASK_ID",
                value_from=k8s.V1EnvFromSource(
                    field_ref=k8s.V1ObjectFieldSelector(
                        field_path="metadata.labels['task_id']",
                    ),
                ),
            ),
        ],
        env_from=[
            k8s.V1EnvFromSource(
                secret_ref=k8s.V1SecretEnvSource(
                    name="airflow-db"
                )
            ),
        ],
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
    )
