from airflow import DAG, Dataset
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator
import kubernetes as k8s


with DAG('DataAwareSchedulingTrigger', start_date=days_ago(1), schedule=[Dataset("gs://local-flyte-test/file.txt")], catchup=False) as dag:
    trigger_from_data_aware_scheduling = python_operator(
        dag=dag,
        name="data-aware-scheduling-trigger",
        repo="navikt/nada-dags",
        script_path="notebooks/read_from_bucket.py",
        requirements_path="notebooks/requirements_write_to_bucket.txt",
        retries=0,
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            image="europe-north1-docker.pkg.dev/nais-management-233d/virksomhetsdatalaget/vdl-airflow@sha256:85e5787aaaf694379fb031954cb53a04a80fcc08934991fcb90fae65102d5fe3",
                        )
                    ]
                ),
            )
        }
    )
