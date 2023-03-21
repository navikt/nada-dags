from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG('bash-operator-eksempel', start_date=datetime(2023, 2, 14), schedule_interval="*/5 * * * *", catchup=False) as dag:

    os.environ["TEST"] = "hallo"

    t1 = BashOperator(
        task_id='notebook',
        bash_command='papermill --log-output ../notebooks/mynb.ipynb ../output.ipynb',
        executor_config={
           "pod_override": k8s.V1Pod(
               spec=k8s.V1PodSpec(
                   containers=[
                      k8s.V1Container(
                         name="base",
                         image="europe-west1-docker.pkg.dev/knada-gcp/knada/airflow-notebooks:2023-03-21-ed0d1e5"
                      )
                   ]
               )
           )
        },
        dag=dag
        )
