"""
1. RODAR EXPERIMENTOS - Outubro 2025

Maria testa vários modelos para encontrar o melhor.
MLflow registra tudo automaticamente.
"""
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
import warnings
warnings.filterwarnings('ignore')

# Tentar importar XGBoost
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

print("🔬 RODANDO EXPERIMENTOS - Outubro 2025")
print("=" * 60)

# Carregar dados
df = pd.read_csv("../dados/outubro_2025.csv")
print(f"\nDataset: {len(df)} transações")
print(f"Fraudes: {df['is_fraud'].sum()} ({df['is_fraud'].sum()/len(df)*100:.1f}%)\n")

# Preparar features
X = df[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y = df["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Configurações de experimentos
experimentos = [
    # RandomForest
    {"nome": "RandomForest (n=100, depth=10)", "model": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)},
    {"nome": "RandomForest (n=200, depth=15)", "model": RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)},
    {"nome": "RandomForest (n=500, depth=20)", "model": RandomForestClassifier(n_estimators=500, max_depth=20, random_state=42)},
    
    # GradientBoosting
    {"nome": "GradientBoosting (n=100, lr=0.1)", "model": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)},
    {"nome": "GradientBoosting (n=200, lr=0.05)", "model": GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, random_state=42)},
    {"nome": "GradientBoosting (n=300, lr=0.1)", "model": GradientBoostingClassifier(n_estimators=300, learning_rate=0.1, random_state=42)},
    
    # LogisticRegression
    {"nome": "LogisticRegression (C=1.0)", "model": LogisticRegression(C=1.0, max_iter=1000, random_state=42)},
    {"nome": "LogisticRegression (C=0.1)", "model": LogisticRegression(C=0.1, max_iter=1000, random_state=42)},
    {"nome": "LogisticRegression (C=10.0)", "model": LogisticRegression(C=10.0, max_iter=1000, random_state=42)},
]

# Adicionar XGBoost se disponível
if HAS_XGBOOST:
    experimentos.insert(3, {"nome": "XGBoost (n=100, lr=0.1)", "model": XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, eval_metric='logloss')})
    experimentos.insert(4, {"nome": "XGBoost (n=200, lr=0.05)", "model": XGBClassifier(n_estimators=200, learning_rate=0.05, random_state=42, eval_metric='logloss')})
    experimentos.insert(5, {"nome": "XGBoost (n=300, lr=0.1)", "model": XGBClassifier(n_estimators=300, learning_rate=0.1, random_state=42, eval_metric='logloss')})

# Configurar MLflow
mlflow.set_tracking_uri("file:../mlruns")
mlflow.set_experiment("deteccao-fraude-outubro-2025")

print("Testando configurações...\n")
resultados = []

for exp in experimentos:
    with mlflow.start_run(run_name=exp["nome"]):
        # Treinar
        model = exp["model"]
        model.fit(X_train, y_train)
        
        # Avaliar
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        
        # Registrar no MLflow
        mlflow.log_params(model.get_params())
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.sklearn.log_model(model, "model")
        
        resultados.append({
            "nome": exp["nome"],
            "f1": f1,
            "run_id": mlflow.active_run().info.run_id
        })
        
        # Mostrar resultado
        destaque = " ⭐" if f1 == max([r["f1"] for r in resultados]) else ""
        print(f"✅ {exp['nome']:40} | F1: {f1:.3f}{destaque}")

# Mostrar vencedor
print("\n" + "=" * 60)
melhor = max(resultados, key=lambda x: x["f1"])
print(f"🏆 VENCEDOR: {melhor['nome']}")
print(f"   F1 Score: {melhor['f1']:.3f}")
print(f"   Run ID: {melhor['run_id'][:12]}")
print(f"\n💾 Todos experimentos salvos no MLflow")
print(f"\n👉 Execute 'mlflow ui' para visualizar")
