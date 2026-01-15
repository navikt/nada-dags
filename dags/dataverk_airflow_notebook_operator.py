from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import notebook_operator
from kubernetes import client


with DAG('DataverkAirflowNotebook', start_date=days_ago(1), schedule="0 8 * * 1-5", catchup=False) as dag:
    nb_op = notebook_operator(
        dag=dag,
        name="nb-op",
        repo="navikt/nada-dags",
        nb_path="notebooks/mynb.ipynb",
        requirements_path="notebooks/requirements.txt",
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}",
        resources=client.V1ResourceRequirements(
            requests={
              "cpu": "1",
              "memory": "1Gi",
            },
            limits={
              "memory": "2Gi",
            }
        ),
    )