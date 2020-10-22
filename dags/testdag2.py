from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta


default_args = {
    'start_date': datetime(2020, 10, 21)
}

with DAG('eriktester', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    t1 = BashOperator(
        task_id='erik',
        bash_command='echo "Erik"',
        dag=dag)
    t2 = BashOperator(
        task_id='tester',
        bash_command='echo "tester"',
        dag=dag)
    t3 = KubernetesPodOperator(
        dag=dag,
        name='test',
        namespace='nada',
        task_id='k8s_task',
        image='busybox',
        cmds=['bash'],
        arguments=["echo", "Hello world"]
    )

    t1 >> t2 >> t3
