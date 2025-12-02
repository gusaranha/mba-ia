"""
EXERCÍCIO 1: MLflow Básico

Objetivo: Registrar um experimento simples com MLflow

Instruções:
- Complete os TODOs na ordem
- Execute o script após cada TODO para ver o resultado
- Abra MLflow UI para verificar o registro

Comandos úteis:
- Executar: python exercicios/exercicio_1_mlflow_basico.py
- Abrir UI: mlflow ui
- Acessar: http://localhost:5000
"""

import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
import pandas as pd

# Carregar dados (já pronto)
df = pd.read_csv("../data/transacoes_processadas.csv")
X = df[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y = df["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ============================================
# TODO 1: Defina o nome do experimento
# ============================================
# Use: mlflow.set_experiment("nome-do-experimento")
# Escolha um nome descritivo, por exemplo: "exercicio-mlflow"

# Seu código aqui:


# ============================================
# TODO 2: Inicie um run com nome descritivo
# ============================================
# Use: with mlflow.start_run(run_name="nome"):
# Todo o código de treino deve ficar DENTRO do with
# Sugestão de nome: "rf_meu_primeiro_run"
#
# ATENÇÃO: Todo o código abaixo (dos TODOs 3-5 e o treino)
# deve ficar INDENTADO dentro do bloco with

# Seu código aqui (não esqueça do : no final):


# Definir parâmetros
n_estimators = 150
max_depth = 12

# ============================================
# TODO 3: Registre os parâmetros
# ============================================
# Use: mlflow.log_param("nome", valor)
# Registre: n_estimators e max_depth

# Seu código aqui:


# Treinar modelo (já pronto)
model = RandomForestClassifier(
    n_estimators=n_estimators, 
    max_depth=max_depth, 
    random_state=42
)
model.fit(X_train, y_train)

# Avaliar (já pronto)
y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

# ============================================
# TODO 4: Registre as métricas
# ============================================
# Use: mlflow.log_metric("nome", valor)
# Registre: f1_score, precision e recall

# Seu código aqui:


# ============================================
# TODO 5: Salve o modelo
# ============================================
# Use: mlflow.sklearn.log_model(model, "model")

# Seu código aqui:


print(f"✅ Experimento registrado!")
print(f"   F1: {f1:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall: {recall:.4f}")


# ============================================
# Após completar todos os TODOs:
# ============================================
# 1. Execute: python exercicios/exercicio_1_mlflow_basico.py
# 2. Execute: mlflow ui
# 3. Abra http://localhost:5000 no navegador
# 4. Verifique se seu run aparece com:
#    - Nome correto
#    - Parâmetros registrados
#    - Métricas registradas
#    - Modelo salvo em Artifacts
