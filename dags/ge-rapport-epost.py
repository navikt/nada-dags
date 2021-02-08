import os
import json
from datetime import timedelta
from airflow import DAG
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_nb_pod_operator


with DAG('ge-rapport-varsling', start_date=days_ago(1), schedule_interval=None) as dag:

    def create_validation_report(results):
        err_msg = ""
        for val_error in results.keys():
            val_res = results[val_error]['result']
            val_args = results[val_error]['expectation_config']['kwargs']
            del val_args['result_format']
            val_type = f"*{results[val_error]['expectation_config']['expectation_type']}* med argumenter {val_args}"
            status = results[val_error]['success']
            err_msg += "\n" \
f"""    _{val_error}_:
            Status: {status}
            Testtype: {val_type}
            Kolonne: {val_args['column']}
            Antall rader: {val_res['element_count']}
            Rader med manglende verdi: {val_res['missing_count']}
            Rader med manglende verdi (%): {val_res['missing_percent']}
            Rader med uventet verdi: {val_res['unexpected_count']}
            Rader med uventet verdi (%): {val_res['unexpected_percent']}
            Utdrag av verdier som feiler test: {val_res['partial_unexpected_list'][:5]}
            """
        return err_msg

    def task_slack_msg(context):
        validate_res = context.get('task_instance').xcom_pull(task_ids='ge-validation')
        slack_msg = f"""
                *Rapport*: Valideringstester med avvik
                *DAG*: {context.get('task_instance').dag_id} 
                *Task*: {context.get('task_instance').task_id}  
                {create_validation_report(validate_res)} 
                """
        varsling = SlackWebhookOperator(
            dag=dag,
            task_id="slack_valideringsresultater",
            webhook_token=os.environ["SLACK_WEBHOOK_TOKEN"],
            message=slack_msg,
            channel="#kubeflow-cron-alerts",
            link_names=True,
            icon_emoji=":page_with_curl:",
            attachments=[{"tests.json": validate_res}],
            provide_context=True,
            proxy=os.environ["HTTPS_PROXY"]
        )
        return varsling.execute(context=context)

    ge_validering = create_knada_nb_pod_operator(dag=dag,
                                                 name="ge-validation",
                                                 repo="navikt/bq-dags",
                                                 nb_path="validate/Validate.ipynb",
                                                 email="erik.vattekar@nav.no",
                                                 namespace="nada",
                                                 branch="main",
                                                 log_output=True,
                                                 delete_on_finish=False,
                                                 retries=0,
                                                 on_success_callback=task_slack_msg,
                                                 do_xcom_push=True,
                                                 retry_delay=timedelta(seconds=5))

    send_epost = EmailOperator(dag=dag,
                               task_id="send_valideringsresultater_epost",
                               to='erik.vattekar@nav.no',
                               subject='GE validering',
                               provide_context=True,
                               html_content="{{ task_instance.xcom_pull(task_ids='ge-validation') }}")

    ge_validering >> send_epost
