"""
GABARITO - EXERCÍCIO 1: MLflow Básico

Este é o gabarito completo do exercício 1.
Use apenas para conferir suas respostas!
"""

import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
import pandas as pd

# Carregar dados
df = pd.read_csv("data/transacoes_processadas.csv")
X = df[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y = df["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# TODO 1: Defina o nome do experimento
mlflow.set_experiment("exercicio-mlflow")

# TODO 2: Inicie um run com nome descritivo
with mlflow.start_run(run_name="rf_meu_primeiro_run"):
    
    # Definir parâmetros
    n_estimators = 150
    max_depth = 12
    
    # TODO 3: Registre os parâmetros
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    
    # Treinar modelo
    model = RandomForestClassifier(
        n_estimators=n_estimators, 
        max_depth=max_depth, 
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Avaliar
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # TODO 4: Registre as métricas
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # TODO 5: Salve o modelo
    mlflow.sklearn.log_model(model, "model")
    
    print(f"✅ Experimento registrado!")
    print(f"   F1: {f1:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall: {recall:.4f}")
