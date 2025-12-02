"""
DEMO 2: Múltiplos experimentos

Demonstra comparação entre:
- Diferentes algoritmos (RandomForest, XGBoost, LogisticRegression, GradientBoosting)
- Diferentes hiperparâmetros para cada algoritmo
"""
import mlflow
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
import pandas as pd

# Tentar importar XGBoost (opcional)
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("⚠️  XGBoost não instalado, usando apenas sklearn")

# Carregar dados
df = pd.read_csv("../data/transacoes_processadas.csv")
X = df[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y = df["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Configurações de experimentos
experimentos = [
    # Random Forest - variações
    {
        "nome": "rf_shallow",
        "algoritmo": "RandomForest",
        "params": {"n_estimators": 50, "max_depth": 5},
        "model_class": RandomForestClassifier
    },
    {
        "nome": "rf_medium",
        "algoritmo": "RandomForest", 
        "params": {"n_estimators": 100, "max_depth": 10},
        "model_class": RandomForestClassifier
    },
    {
        "nome": "rf_deep",
        "algoritmo": "RandomForest",
        "params": {"n_estimators": 200, "max_depth": 20},
        "model_class": RandomForestClassifier
    },
    {
        "nome": "rf_large",
        "algoritmo": "RandomForest",
        "params": {"n_estimators": 500, "max_depth": 15},
        "model_class": RandomForestClassifier
    },
    # Gradient Boosting - variações
    {
        "nome": "gb_conservative",
        "algoritmo": "GradientBoosting",
        "params": {"n_estimators": 50, "max_depth": 3, "learning_rate": 0.1},
        "model_class": GradientBoostingClassifier
    },
    {
        "nome": "gb_balanced",
        "algoritmo": "GradientBoosting",
        "params": {"n_estimators": 100, "max_depth": 5, "learning_rate": 0.1},
        "model_class": GradientBoostingClassifier
    },
    {
        "nome": "gb_aggressive",
        "algoritmo": "GradientBoosting",
        "params": {"n_estimators": 200, "max_depth": 7, "learning_rate": 0.05},
        "model_class": GradientBoostingClassifier
    },
    # Logistic Regression - variações
    {
        "nome": "lr_default",
        "algoritmo": "LogisticRegression",
        "params": {"C": 1.0, "max_iter": 1000},
        "model_class": LogisticRegression
    },
    {
        "nome": "lr_regularized",
        "algoritmo": "LogisticRegression",
        "params": {"C": 0.1, "max_iter": 1000},
        "model_class": LogisticRegression
    },
    {
        "nome": "lr_loose",
        "algoritmo": "LogisticRegression",
        "params": {"C": 10.0, "max_iter": 1000},
        "model_class": LogisticRegression
    },
]

# Adicionar XGBoost se disponível
if HAS_XGBOOST:
    experimentos.extend([
        {
            "nome": "xgb_light",
            "algoritmo": "XGBoost",
            "params": {"n_estimators": 50, "max_depth": 3, "learning_rate": 0.1},
            "model_class": XGBClassifier
        },
        {
            "nome": "xgb_medium",
            "algoritmo": "XGBoost",
            "params": {"n_estimators": 100, "max_depth": 5, "learning_rate": 0.1},
            "model_class": XGBClassifier
        },
        {
            "nome": "xgb_heavy",
            "algoritmo": "XGBoost",
            "params": {"n_estimators": 200, "max_depth": 7, "learning_rate": 0.05},
            "model_class": XGBClassifier
        },
    ])

# Configurar experimento
mlflow.set_experiment("deteccao-fraude")

print(f"🚀 Executando {len(experimentos)} experimentos...\n")
print("-" * 70)

resultados = []

for exp in experimentos:
    with mlflow.start_run(run_name=exp["nome"]):
        
        # Registrar parâmetros
        mlflow.log_param("algoritmo", exp["algoritmo"])
        mlflow.log_params(exp["params"])
        
        # Treinar
        if exp["algoritmo"] == "XGBoost":
            model = exp["model_class"](**exp["params"], random_state=42, eval_metric='logloss')
        else:
            model = exp["model_class"](**exp["params"], random_state=42)
        
        model.fit(X_train, y_train)
        
        # Avaliar
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        
        # Salvar modelo
        mlflow.sklearn.log_model(model, "model")
        
        resultados.append({
            "nome": exp["nome"],
            "algoritmo": exp["algoritmo"],
            "f1": f1
        })
        
        print(f"✅ {exp['nome']:20} | {exp['algoritmo']:18} | F1: {f1:.4f}")

print("-" * 70)

# Mostrar ranking
print("\n🏆 RANKING POR F1 SCORE:\n")
resultados_sorted = sorted(resultados, key=lambda x: x["f1"], reverse=True)
for i, r in enumerate(resultados_sorted[:5], 1):
    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
    print(f"{medal} {i}. {r['nome']:20} | {r['algoritmo']:18} | F1: {r['f1']:.4f}")

print(f"\n👉 Execute 'mlflow ui' e acesse http://localhost:5000")
print("   - Ordene por f1_score para ver o melhor")
print("   - Compare experimentos lado a lado")
