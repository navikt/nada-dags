from custom_dag import CustomDag2

with CustomDag2("asdf") as dag:
    t1 = dag.create_python_operator()
    t2 = dag.create_python_operator()

    t1 >> t2
