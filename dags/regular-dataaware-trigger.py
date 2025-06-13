from airflow.utils.dates import days_ago
from kubernetes import client as k8s
from airflow.datasets import Dataset
from airflow.decorators import dag, task


@dag(
    dag_id="RegularDataAwareTrigger",
    dag_display_name="RegularDataAwareTrigger",
    start_date=days_ago(1),
    schedule_interval=None,
    schedule=[Dataset("gs://local-flyte-test/file.txt")],
    catchup=False,
)
def trigger_test():
    @task(
        # executor_config={
        #     "pod_override": k8s.V1Pod(
        #         spec=k8s.V1PodSpec(
        #             containers=[
        #                 k8s.V1Container(
        #                     name="base",
        #                     image="europe-north1-docker.pkg.dev/nais-management-233d/virksomhetsdatalaget/vdl-airflow@sha256:85e5787aaaf694379fb031954cb53a04a80fcc08934991fcb90fae65102d5fe3",
        #                 )
        #             ]
        #         ),
        #     )
        # },
    )
    def transfer():
        print("triggered by data aware scheduling")
  
    transfer()
