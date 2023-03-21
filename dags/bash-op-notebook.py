from airflow import DAG
from airflow.operators.kubernetes_operator import KubernetesPodOperator
from datetime import datetime
from datetime import datetime
from airflow.utils.dates import days_ago
from kubernetes import client as k8s


with DAG('kube-operator-notebook', start_date=days_ago(1), schedule_interval=None, catchup=False) as dag:

    t1 = KubernetesPodOperator(
        init_containers=[
            name="clone-repo",
            image=os.getenv("CLONE_REPO_IMAGE", "europe-west1-docker.pkg.dev/knada-gcp/knada/git-sync:2023-03-08-80342e3"),
            volume_mounts=[
            k8s.V1VolumeMount(
                name="dags-data", mount_path=mount_path, sub_path=None, read_only=False
            ),
            k8s.V1VolumeMount(
                name="airflow-git-secret",
                mount_path="/keys",
                sub_path=None,
                read_only=False,
            ),
        ],
        command=["/bin/sh", "-c"],
        args=[f"/git-clone.sh {repo} {branch} {mount_path}; chmod -R 777 {mount_path}"],   
        ]
        task_id='notebook',
        cmds=["bash", "-c"],
        arguments=["papermill", "--log-output", "/dags/notebooks/mynb.ipynb", "/dags/output.ipynb"],
        image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-notebooks:2023-03-08-d3684b7",
        dag=dag,
        volume_mounts=[
            k8s.V1VolumeMount(
                name="dags-data",
                mount_path="/dags",
                sub_path=None,
                read_only=False
        ),
            k8s.V1VolumeMount(
                name="ca-bundle-pem",
                mount_path=CA_BUNDLE_PATH,
                read_only=True,
                sub_path="ca-bundle.pem"
            )
        ]
        volumes=[
            k8s.V1Volume(
                name="dags-data"
            ),
            k8s.V1Volume(
                name="airflow-git-secret",
                secret=V1SecretVolumeSource(
                    default_mode=448,
                    secret_name=os.getenv("K8S_GIT_CLONE_SECRET", "github-app-secret"),
                )
            ),
            k8s.V1Volume(
                name="ca-bundle-pem",
                config_map=V1ConfigMapVolumeSource(
                    default_mode=420,
                    name="ca-bundle-pem",
                )
            ),
        ]
    )
