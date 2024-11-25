from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow import python_operator
from airflow.providers.slack.operators.slack import SlackAPIPostOperator


def on_success_callback(context):
    SlackAPIPostOperator(
            task_id="airflow_task_success_slack",
            slack_conn_id="slack_connection",
            text=f":checked: Tester on success callback",
            channel="#nada-test",
    ).execute(context)


# Ved bruk av KubernetesPodOperators er worker podden som poster slack notifikasjoner i on_failure/on_success callbacks 
# ikke den samme podden som kjører den faktiske brukerkoden.
# Denne testen er for å verifisere at allowlist blir satt riktig, for riktig pod, for en on_success callback
# som skal poste til slack. Dette vil fungere likt for den innebygde on_failure callbacken i dataverk-airflow.
with DAG('DataverkAirflowSlackNotificationCallbacks', start_date=days_ago(1), schedule="10 10 * * 1-5", catchup=False) as dag:
    py_op = python_operator(
        dag=dag,
        name="python-op",
        repo="navikt/nada-dags",
        script_path="notebooks/dummyscript.py",
        retries=0,
        on_success_callback=on_success_callback,
        slack_channel="{{ var.value.get('SLACK_ALERT_CHANNEL') }}", # Denne må settes for at dataverk-airflow skal legge til slack i allowlist
    )
