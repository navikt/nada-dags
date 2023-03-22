from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from kubernetes import client as k8s

with DAG('knaudit_example', start_date=datetime(2023, 3, 9)) as dag:

    task_1 = KubernetesPodOperator(
        name="knaudit",
        task_id="task-one",
        get_logs=True,
        image="europe-west1-docker.pkg.dev/knada-gcp/knada/knaudit:2023-03-16-f8353eb",
        env_vars=[
            k8s.V1EnvVar(
                name="ELASTICSEARCH_URL",
                value="https://log-ingest.adeo.no",
            ),
            k8s.V1EnvVar(
                name="ELASTICSEARCH_INDEX",
                value="tjenestekall-knada-airflow-run-audit",
            ),
            k8s.V1EnvVar(
                name="CA_CERT_PATH",
                value="/etc/pki/tls/certs/ca-bundle.crt",
            ),
            k8s.V1EnvVar(
                name="GIT_REPO_PATH",
                value="/dags",
            ),
            k8s.V1EnvVar(
                name="AIRFLOW_RUN_ID",
                value="test av knaudit"
            ),
            k8s.V1EnvVar(
                name="NAMESPACE",
                value_from=k8s.V1EnvVarSource(
                    field_ref=k8s.V1ObjectFieldSelector(
                        field_path="metadata.namespace",
                    ),
                ),
            ),
            k8s.V1EnvVar(
                name="AIRFLOW_DAG_ID",
                value_from=k8s.V1EnvVarSource(
                    field_ref=k8s.V1ObjectFieldSelector(
                        field_path="metadata.labels['dag_id']",
                    ),
                ),
            ),
            k8s.V1EnvVar(
                name="AIRFLOW_TASK_ID",
                value_from=k8s.V1EnvVarSource(
                    field_ref=k8s.V1ObjectFieldSelector(
                        field_path="metadata.labels['task_id']",
                    ),
                ),
            ),
            k8s.V1EnvVar(
                name="AIRFLOW_DB_URL",
                value_from=k8s.V1EnvVarSource(
                    secret_key_ref=k8s.V1SecretKeySelector(
                        name="airflow-db",
                        key="connection"
                    ),
                ),
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
            )
        ],
        security_context={
            "fsGroup": 0,
            "runAsUser": 50000,
            "runAsNonRoot": True,
        }
    )
