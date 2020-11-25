from airflow import DAG
from datetime import timedelta
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator
from airflow.utils.dates import days_ago


with DAG('gcs-bigquery-eksempel', start_date=days_ago(-1), schedule_interval="15 8 * * *") as dag:
    read_ssb_store_gcs = create_knada_nb_pod_operator(dag=dag,
                                                      name="read-ssb-write-gcs",
                                                      repo="navikt/nada-dags",
                                                      nb_path="notebooks/FetchStyrkUploadGCS.ipynb",
                                                      email="erik.vattekar@nav.no",
                                                      namespace="nada",
                                                      branch="main",
                                                      log_output=True,
                                                      retries=1,
                                                      retry_delay=timedelta(seconds=5))

    read_gcs_process_store_gbq = create_knada_nb_pod_operator(dag=dag,
                                                              name="read-gcs-process-write-gbq",
                                                              repo="navikt/nada-dags",
                                                              nb_path="notebooks/GcsToBigQuery.ipynb",
                                                              email="erik.vattekar@nav.no",
                                                              namespace="nada",
                                                              branch="main",
                                                              log_output=True,
                                                              retries=1,
                                                              retry_delay=timedelta(seconds=5))

    read_ssb_store_gcs >> read_gcs_process_store_gbq
