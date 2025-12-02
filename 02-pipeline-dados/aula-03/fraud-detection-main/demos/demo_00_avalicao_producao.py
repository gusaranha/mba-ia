from datetime import datetime, timedelta
from sklearn.metrics import f1_score
import pandas as pd

LIMIAR = 0.85

def query(sql):
    # import psycopg2
    # conn = psycopg2.connect(
    #     host="prod-db.empresa.com",
    #     database="ml_producao",
    #     user=os.getenv("DB_USER"),
    #     password=os.getenv("DB_PASS")
    # )
    # return pd.read_sql(sql, conn)
    pass

def insert(tabela, dados):
    # import psycopg2
    # conn = psycopg2.connect(...)
    # cursor = conn.cursor()
    # cursor.execute(
    #     f"INSERT INTO {tabela} (data, f1) VALUES (%s, %s)",
    #     (dados['data'], dados['f1'])
    # )
    # conn.commit()
    pass

def alertar_equipe(mensagem):
    # import requests
    # requests.post(
    #     "https://hooks.slack.com/services/XXX/YYY/ZZZ",
    #     json={"text": mensagem, "channel": "#ml-alertas"}
    # )
    print(f"[ALERTA] {mensagem}")

def avaliar_modelo_producao():
    hoje = datetime.now().date()
    data_inicio = hoje - timedelta(days=37)
    data_fim = hoje - timedelta(days=7)
    
    predicoes = query(f"""
        SELECT transacao_id, predicao, data_predicao
        FROM log_predicoes
        WHERE data_predicao BETWEEN '{data_inicio}' AND '{data_fim}'
    """)
    
    labels = query(f"""
        SELECT transacao_id, foi_fraude AS label
        FROM transacoes
        WHERE data_confirmacao BETWEEN '{data_inicio}' AND '{data_fim}'
    """)
    
    dados = predicoes.merge(labels, on='transacao_id')
    
    f1 = f1_score(dados['label'], dados['predicao'])
    
    insert("metricas_producao", {'data': hoje, 'f1': f1})
    
    if f1 < LIMIAR:
        alertar_equipe(f"F1 caiu para {f1:.3f}! Verificar modelo.")

if __name__ == "__main__":
    avaliar_modelo_producao()