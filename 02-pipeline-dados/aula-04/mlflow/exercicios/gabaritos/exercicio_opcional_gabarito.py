"""
GABARITO - EXERCÍCIO OPCIONAL: Múltiplos Runs

Este é o gabarito completo do exercício opcional.
Use apenas para conferir suas respostas!
"""

import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import pandas as pd

# Carregar dados
df = pd.read_csv("data/transacoes_processadas.csv")
X = df[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y = df["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# TODO 1: Lista de configurações
configs = [
    {"n_estimators": 100, "max_depth": 5},
    {"n_estimators": 150, "max_depth": 10},
    {"n_estimators": 200, "max_depth": 15},
]

# TODO 2: Configurar experimento
mlflow.set_experiment("exercicio-multiplos")

# TODO 3: Loop para testar cada configuração
print("🚀 Testando configurações...\n")

for config in configs:
    with mlflow.start_run(run_name=f"rf_n{config['n_estimators']}_d{config['max_depth']}"):
        
        # Registrar parâmetros
        mlflow.log_params(config)
        
        # Treinar
        model = RandomForestClassifier(**config, random_state=42)
        model.fit(X_train, y_train)
        
        # Avaliar
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred)
        
        # Registrar métrica
        mlflow.log_metric("f1_score", f1)
        
        # Salvar modelo
        mlflow.sklearn.log_model(model, "model")
        
        print(f"✅ Config {config}: F1 = {f1:.4f}")

print("\n" + "="*50)
print("Execute 'mlflow ui' e acesse http://localhost:5000")
print("Ordene por f1_score para encontrar o melhor!")
print("="*50)
