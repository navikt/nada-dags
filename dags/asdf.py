from custom_dag import CustomDag

with CustomDag("asdf") as dag:
    t1 = dag.create_python_operator()
