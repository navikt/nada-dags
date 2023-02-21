from airflow import DAG
from airflow.operators.email import EmailOperator

with DAG(dag_id="epost", start_date=datetime(2023, 2, 21)) as dag:
    
    epost = EmailOperator(
        task_id="send-epost",
        to=["Kyrre.Havik@nav.no"],
        subject="Hei, fra Airflow",
        html_content="<h1>Hello world</h1><p>Dette er en e-post sendt fra en Airflow DAG</p>",
    )
