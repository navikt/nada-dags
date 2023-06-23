# NADA Dags

Repo med eksempler på å kjøre jobber i Airflow.

## Enkle operators
De enkleste operatorene å bruke er [BashOperator](https://github.com/navikt/nada-dags/blob/main/dags/bash_operator.py) og [PythonOperator](https://github.com/navikt/nada-dags/blob/main/dags/pyoperator.py). Disse bør i de fleste tilfeller dekke behovet for airflow DAGs. Men merk at ingen av disse vil fungere dersom koden som skal kjøres finnes i et annet repo enn teamets `dag` repo. Er så tilfellet, se [pod operators](#pod-operators).

## Notifikasjoner
I `dags` mappen finner du eksempel på både [slack notifikasjon](https://github.com/navikt/nada-dags/blob/main/dags/slack_operator.py) og [epost notifikasjon](https://github.com/navikt/nada-dags/blob/main/dags/email-operator.py)

## Pod operators
Ønsker man å kjøre `KubernetesPodOperators` anbefales det å kopiere innholdet i mappen [common](https://github.com/navikt/nada-dags/tree/main/common) inn i deres eget dags repo og importere fra denne i deres DAGs. Denne python modulen har en factory funksjon for å lage `KubernetesPodOperators` tilsvarende det man fikk tidligere gjennom `dataverk-airflow` biblioteket. For eksempel på bruk av denne common-modulen, se [her](https://github.com/navikt/nada-dags/blob/main/dags/common_podoperator_example.py).

Ønsker en ikke å bruke denne felles modulen finnes det et enkelt eksempel på en `KubernetesPodOperator` [her](https://github.com/navikt/nada-dags/blob/main/dags/kubernetes_pod_operator.py).
