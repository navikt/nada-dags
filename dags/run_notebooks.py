from airflow import DAG

with DAG('run-notebook', start_date="2023-03-21", schedule_interval="0 10 * * *") as dag:
    t1 = BashOperator(
        task_id="hello-world",
        bash_command="papermill --log-output ../notebooks/mynb.ipynb output.ipynb",
        executor_config={
           "pod_override": k8s.V1Pod(
               spec=k8s.V1PodSpec(
                   containers=[
                      k8s.V1Container(
                         name="base",
                         image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-notebooks:2023-03-08-d3684b7"
                      )
                   ]
               )
           )
        }
    )
