from airflow.utils.dates import days_ago
from airflow import DAG
from common.podop_factory import create_pod_operator
from kubernetes import client

dag_name = 'test-xcom'

# default_args = {
#     'owner': 'erik',
#     'start_date': datetime(2023, 6, 6),
#     # 'depends_on_past': False,
#     # If a task fails, retry it once after waiting at least 5 minutes
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }


with DAG(dag_name, start_date=days_ago(1), schedule_interval=None) as dag:

    test_task = create_pod_operator(
        dag=dag,
        name="test_task",
        repo="navikt/nada-dags",
        nb_path="test_notebook.ipynb",
        slack_channel="#kubeflow-cron-alerts",
        branch="main",
        log_output=True,
        retries=0,
        do_xcom_push=True,
        delete_on_finish=False,
        resources=client.V1ResourceRequirements(
            requests={
                "memory": "256M"
            },
            limits={
                "memory": "256M"
            },
        )
    )


    test_task