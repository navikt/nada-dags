import os
from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from kubernetes import client as k8s

MOUNT_PATH = "/code"
REPO = "navikt/nada-airflow"
BRANCH = "main"

def run():
    from kode.modul import mycallable
    mycallable()

with DAG('ExtraInitContainerExample', start_date=days_ago(1), schedule_interval=None) as dag:    
    run_this = PythonOperator(
    task_id='test-pythonoperator',
    python_callable=run,
    executor_config={
        "pod_override": k8s.V1Pod(
            spec=k8s.V1PodSpec(
                init_containers=[
                    k8s.V1Container(
                        name="clone-code-repo",
                        image=os.getenv("CLONE_REPO_IMAGE"),
                        command=["/bin/sh", "-c"],
                        args=[f"/git-clone.sh {REPO} {BRANCH} {MOUNT_PATH}"],
                        volume_mounts=[
                            k8s.V1VolumeMount(
                                name="code", mount_path=MOUNT_PATH, sub_path=None, read_only=False
                            ),
                            k8s.V1VolumeMount(
                                name="github-app-secret",
                                mount_path="/keys",
                                sub_path=None,
                                read_only=False,
                            ),
                        ],
                        security_context=k8s.V1SecurityContext(
                            allow_privilege_escalation=False,
                            run_as_user=50000,
                        )
                    )
                ],
                containers=[
                    k8s.V1Container(
                       name="base",
                       image=os.getenv("KNADA_AIRFLOW_OPERATOR_IMAGE"),
                       env=[
                           k8s.V1EnvVar("PYTHONPATH", MOUNT_PATH)
                       ],
                       volume_mounts=[
                            k8s.V1VolumeMount(
                                name="code", mount_path=MOUNT_PATH, sub_path=None, read_only=False
                            ),
                       ],
                        security_context=k8s.V1SecurityContext(
                            allow_privilege_escalation=False,
                            run_as_user=50000,
                        )
                    )
                ],
                volumes= [
                    k8s.V1Volume(
                        name="code"
                    )
                ],
                security_context=k8s.V1PodSecurityContext(
                    fs_group=0,
                    run_as_non_root=True,
                    seccomp_profile=k8s.V1SeccompProfile(
                        type="RuntimeDefault"
                    )
                ),
            )
        )
    },
    dag=dag)
