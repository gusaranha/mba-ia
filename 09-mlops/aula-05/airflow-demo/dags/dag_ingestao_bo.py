# Aula 04 -- DAG (Directed Acyclic Graph / Grafo Acíclico Dirigido) que
# executa o ETL (Extract, Transform, Load) de ingestão dos BOs do
# projeto-guia PCDF.
#
# Onde isso roda: DENTRO do container airflow-worker (ou do scheduler,
# se o executor for local), nunca na sua maquina diretamente. Os
# arquivos .csv so aparecem "fora" porque a pasta ./data foi montada
# como volume (ver docker-compose.override.yml).
#
# Salvar em: airflow-run/dags/dag_ingestao_bo.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd


def extract(**kw):
    """E de ETL -- le o arquivo bruto gerado na Pendência 2 da Aula 03."""
    df = pd.read_csv("/opt/airflow/data/bos_sinteticos.csv")
    kw["ti"].xcom_push(key="raw", value=df.to_json())


def clean(**kw):
    """T de ETL -- normaliza o texto do relato (lowercase + strip).
    O XCom (Cross-Communication) e o mecanismo do Airflow para passar
    dados pequenos entre tasks do mesmo DAG."""
    raw = kw["ti"].xcom_pull(key="raw")
    df = pd.read_json(raw)
    df["texto_relato"] = df["texto_relato"].str.lower().str.strip()
    kw["ti"].xcom_push(key="clean", value=df.to_json())


def load(**kw):
    """L de ETL -- grava o resultado tratado, pronto para as próximas
    aulas (Kubeflow, CI/CD, observabilidade)."""
    clean_data = kw["ti"].xcom_pull(key="clean")
    df = pd.read_json(clean_data)
    df.to_csv("/opt/airflow/data/bos_tratados.csv", index=False)


with DAG(
    "ingestao_bo_pcdf",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="clean", python_callable=clean)
    t3 = PythonOperator(task_id="load", python_callable=load)
    t1 >> t2 >> t3
