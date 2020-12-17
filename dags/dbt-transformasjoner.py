from airflow import DAG
from dataverk_airflow.knada_operators import create_knada_dbt_run_operator
from airflow.utils.dates import days_ago


with DAG('dbt-transformasjoner', start_date=days_ago(0), schedule_interval=None) as dag:
    dbt_run = create_knada_dbt_run_operator(dag,
                                            name="dbt-run",
                                            repo="navikt/bq-dags",
                                            namespace="nada",
                                            dbt_dir="styrk",
                                            email="erik.vattekar@nav.no",
                                            branch="main")
