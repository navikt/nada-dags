import pendulum
from kubernetes.client import models as k8s
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow'
}

with DAG(
        dag_id='LargePodRequest',
        default_args=default_args,
        schedule=None,
        is_paused_upon_creation=True,
        start_date=pendulum.today('UTC').add(days=-2),
        max_active_runs=1,
        catchup=False,
        tags=['k8s-pod-operator', 'huge-task'],
) as dag:
    k = KubernetesPodOperator(
        image="ubuntu:noble-20240429",
        cmds=["bash", "-cx"],
        arguments=["echo hello"],
        name="k8s-pod",
        task_id="huge-pod",
        hostnetwork=False,
        get_logs=True,
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
        # https://cloud.google.com/kubernetes-engine/docs/how-to/node-auto-provisioning#custom_machine_family
        affinity=k8s.V1Affinity(
            node_affinity=k8s.V1NodeAffinity(
                required_during_scheduling_ignored_during_execution=k8s.V1NodeSelector(
                    node_selector_terms=[
                        k8s.V1NodeSelectorTerm(
                            match_expressions=[
                                k8s.V1NodeSelectorRequirement(key="cloud.google.com/machine-family", operator="In", values=["n2"])
                            ]
                        )
                    ]
                ),
            ),
        )
    )
