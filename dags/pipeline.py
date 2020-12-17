from airflow import DAG
from datetime import datetime, timedelta
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator, create_knada_dbt_seed_operator, \
    create_knada_dbt_run_operator

with DAG('pipeline-eksempel', start_date=datetime(2020, 11, 9), schedule_interval=None) as dag:
    validate = create_knada_nb_pod_operator(dag=dag,
                                            name="ge-validation",
                                            repo="navikt/bq-dags",
                                            nb_path="validate/Validate.ipynb",
                                            email="erik.vattekar@nav.no",
                                            namespace="nada",
                                            branch="main",
                                            log_output=True,
                                            retries=0,
                                            retry_delay=timedelta(seconds=5))

    seed_s3 = create_knada_dbt_seed_operator(dag,
                                             name="upload-s3-blob-to-bq",
                                             repo="navikt/bq-dags",
                                             namespace="nada",
                                             dbt_dir="styrk",
                                             seed_source={"host": "s3",
                                                          "bucket": "nav-opendata",
                                                          "blob_name": "styrk-koder/styrk_s3.csv"},
                                             email="erik.vattekar@nav.no",
                                             branch="main")

    transformations = create_knada_dbt_run_operator(dag,
                                                    name="dbt-transformations",
                                                    repo="navikt/bq-dags",
                                                    namespace="nada",
                                                    dbt_dir="styrk",
                                                    email="erik.vattekar@nav.no",
                                                    branch="main")

    validate >> seed_s3 >> transformations
