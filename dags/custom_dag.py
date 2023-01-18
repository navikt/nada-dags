from airflow import DAG
from airflow.utils.dates import days_ago
from dataverk_airflow.knada_operators import create_knada_python_pod_operator

class CustomDag:
    def __init__(self, name) -> None:
        self.dag = DAG(
            dag_id=name,
            description=self._repo,
            schedule_interval=None,
            catchup=False,
            start_date=days_ago(1)
        )
        
    def __enter__(self):
        self.dag.__enter__()
        return self


    def __exit__(self, _type, _value, _tb):
        self.dag.__exit__(_type, _value, _tb)

    def create_python_operator(self):
        return create_knada_python_pod_operator(dag=self.dag,
                name="knada-pod-operator",
                repo="navikt/nada-dags",
                nb_path="notebooks/mynb.ipynb",
                branch="main",
                delete_on_finish=False,
                log_output=True
        )

class CustomDag2(DAG):
    def __init__(self, name) -> None:
        super().__init__(
            dag_id=name,
            description=self._repo,
            schedule_interval=None,
            catchup=False,
            start_date=days_ago(1)
        )

    def __enter__(self):
        super().__enter__()
        return self


    def __exit__(self, _type, _value, _tb):
        super().__exit__(_type, _value, _tb)

    def create_python_operator(self):
        return create_knada_python_pod_operator(dag=self,
                name="knada-pod-operator",
                repo="navikt/nada-dags",
                nb_path="notebooks/mynb.ipynb",
                branch="main",
                delete_on_finish=False,
                log_output=True
        )
