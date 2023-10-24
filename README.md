# NADA Dags

Repo med eksempler på hvordan forskjellige Airflow operators kan brukes.

## Enkle operators

De enkleste operatorene å bruke er [BashOperator](https://github.com/navikt/nada-dags/blob/main/dags/bash_operator.py) og [PythonOperator](https://github.com/navikt/nada-dags/blob/main/dags/pyoperator.py).
Disse bør de flestes behovet for Airflow DAGs.
Merk at ingen av de offisielle operatorene vil fungere dersom koden som skal kjøres finnes i et annet repo enn teamets `dag` repo.
Har man DAGs definisjoner i et repo og selve koden som skal kjøres i et annet repo kan man bruke [Dataverk Airflow](#dataverk-airflow) i stedet.

## Dataverk Airflow

For å forenkle det å kjøre Airflow Dags har vi lagd [Dataverk Airflow](https://pypi.org/project/dataverk-airflow/), som er en gruppe operators som alle lar deg klone et ekstern repo, og installere Python-pakker ved oppstart.
Operators vi har støtte for er `Python`, `Notebook`, og `Quarto`.
Vi har også overskrevet `KubernetesPodOperator` som har støtte for kloning, og installasjon av Python pakker, mens ellers ikke gjøre noe spesielt.

## Notifikasjoner

I `dags` mappen finner du eksempel på både [Slack notifikasjon](https://github.com/navikt/nada-dags/blob/main/dags/slack_operator.py) og [E-post notifikasjon](https://github.com/navikt/nada-dags/blob/main/dags/email_operator.py)
