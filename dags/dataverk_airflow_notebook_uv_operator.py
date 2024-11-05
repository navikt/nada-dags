from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import notebook_operator


with DAG('DataverkAirflowNotebookUV', start_date=days_ago(1), schedule="0 8 * * 1-5", catchup=False) as dag:
    nb_op_uv = notebook_operator(
        dag=dag,
        name="nb-op-uv",
        repo="navikt/nada-dags",
        nb_path="notebooks/mynb.ipynb",
        requirements_path="notebooks/requirements.txt",
        slack_channel="#nada-alerts",
        use_uv_pip_install=True,
    )
