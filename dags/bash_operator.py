import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('BashOperator', start_date=datetime(2023, 2, 14), schedule=None) as dag:

    os.environ['WORLD'] = 'Mars'

    t1 = BashOperator(
        task_id='hello_task',
        bash_command='echo "Hello $WORLD at $(date)"'
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    init_containers=[
                        k8s.V1Container(
                            name="clone-code-repo",
                            image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-papermill:2023-06-22-9732e6c",
                        )
                    ]
                )
            )
        }
    )

    t2 = BashOperator(
        task_id='bye_task',
        bash_command='echo "Bye $WORLD"',
        env={
            'WORLD': 'Earth'
        })

    t1 >> t2
