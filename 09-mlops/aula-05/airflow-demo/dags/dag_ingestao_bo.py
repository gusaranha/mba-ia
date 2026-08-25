from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from io import StringIO

import pandas as pd


def extract(**kw):
    df = pd.read_csv("/opt/airflow/data/bos_sinteticos.csv")

    kw["ti"].xcom_push(
        key="raw",
        value=df.to_json()
    )


def clean(**kw):
    raw = kw["ti"].xcom_pull(
        task_ids="extract",
        key="raw"
    )

    if raw is None:
        raise ValueError("XCom 'raw' da task 'extract' não encontrado")

    df = pd.read_json(StringIO(raw))

    df["texto_relato"] = (
        df["texto_relato"]
        .str.lower()
        .str.strip()
    )

    kw["ti"].xcom_push(
        key="clean",
        value=df.to_json()
    )


def load(**kw):
    clean_data = kw["ti"].xcom_pull(
        task_ids="clean",
        key="clean"
    )

    if clean_data is None:
        raise ValueError("XCom 'clean' da task 'clean' não encontrado")

    df = pd.read_json(StringIO(clean_data))

    df.to_csv(
        "/opt/airflow/data/bos_tratados.csv",
        index=False
    )


with DAG(
    "ingestao_bo_pcdf",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="extract",
        python_callable=extract
    )

    t2 = PythonOperator(
        task_id="clean",
        python_callable=clean
    )

    t3 = PythonOperator(
        task_id="load",
        python_callable=load
    )

    t1 >> t2 >> t3