"""
EXERCÍCIO OPCIONAL: Múltiplos Runs

Objetivo: Testar várias configurações e encontrar a melhor

Instruções:
- Modifique este código para testar 3 configurações diferentes
- Use um loop para registrar cada experimento
- Depois, abra mlflow ui e encontre o melhor modelo

Tempo estimado: 15 minutos
"""

import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import pandas as pd

# Carregar dados (já pronto)
df = pd.read_csv("data/transacoes_processadas.csv")
X = df[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y = df["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ============================================
# TODO 1: Defina uma lista de configurações
# ============================================
# Crie uma lista com 3 dicionários, cada um com:
# - n_estimators: número de árvores (ex: 100, 150, 200)
# - max_depth: profundidade máxima (ex: 5, 10, 15)
#
# Exemplo:
# configs = [
#     {"n_estimators": ???, "max_depth": ???},
#     {"n_estimators": ???, "max_depth": ???},
#     {"n_estimators": ???, "max_depth": ???},
# ]

# Seu código aqui:
configs = [
    # Complete com 3 configurações diferentes
]


# ============================================
# TODO 2: Configure o experimento
# ============================================
# Use: mlflow.set_experiment("nome")

# Seu código aqui:


# ============================================
# TODO 3: Crie um loop para testar cada configuração
# ============================================
# Para cada config na lista:
# - Inicie um run com nome único (dica: use f"rf_n{config['n_estimators']}")
# - Registre os parâmetros
# - Treine o modelo
# - Calcule e registre o F1
# - Salve o modelo

# Seu código aqui:
for config in configs:
    # Dica: use with mlflow.start_run(run_name=f"rf_n{config['n_estimators']}"):
    pass  # Remova esta linha e adicione seu código


# ============================================
# Após completar:
# ============================================
# 1. Execute: python exercicios/exercicio_opcional_multiplos.py
# 2. Execute: mlflow ui
# 3. Acesse http://localhost:5000
# 4. Ordene por f1_score (clique no cabeçalho da coluna)
# 5. Identifique qual configuração teve o melhor resultado
# 6. Compare 2 runs lado a lado (selecione e clique "Compare")

print("\n" + "="*50)
print("Após executar, abra mlflow ui e responda:")
print("- Qual configuração teve o melhor F1?")
print("- Aumentar n_estimators sempre melhora o resultado?")
print("="*50)
