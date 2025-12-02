"""
DEMO 3: Carregar o melhor modelo do MLflow

Demonstra como:
- Buscar experimentos programaticamente
- Encontrar o melhor modelo por métrica
- Carregar e usar o modelo para predições
"""
import mlflow
import pandas as pd

EXPERIMENT_NAME = "deteccao-fraude"

# 1. Buscar o experimento
print("🔍 Buscando experimento...")
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

if experiment is None:
    print(f"❌ Experimento '{EXPERIMENT_NAME}' não encontrado.")
    print("   Execute primeiro: python demos/demo_2_multiplos_experimentos.py")
    exit(1)

# 2. Listar runs ordenados por F1
print("📊 Listando runs ordenados por F1 score...\n")
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_score DESC"]
)

if len(runs) == 0:
    print("❌ Nenhum run encontrado no experimento.")
    exit(1)

# Mostrar top 5
print("TOP 5 MODELOS:")
print("-" * 70)
cols = ["run_id", "params.algoritmo", "metrics.f1_score", "metrics.precision", "metrics.recall"]
display_cols = [c for c in cols if c in runs.columns]
print(runs[display_cols].head(5).to_string(index=False))
print("-" * 70)

# 3. Pegar o ID do melhor
best_run_id = runs.iloc[0]["run_id"]
best_f1 = runs.iloc[0]["metrics.f1_score"]
best_algo = runs.iloc[0].get("params.algoritmo", "Desconhecido")

print(f"\n🏆 Melhor modelo:")
print(f"   Run ID: {best_run_id}")
print(f"   Algoritmo: {best_algo}")
print(f"   F1 Score: {best_f1:.4f}")

# 4. Carregar o modelo
print(f"\n📦 Carregando modelo...")
model = mlflow.sklearn.load_model(f"runs:/{best_run_id}/model")
print(f"   Tipo: {type(model).__name__}")
print(f"   ✅ Modelo carregado com sucesso!")

# 5. Fazer predições com dados novos
print("\n🔮 Testando predições com dados novos:\n")

novos_dados = pd.DataFrame([
    {"valor": 150.00, "hora": 14, "categoria_cod": 2, "qtd_transacoes_24h": 2},   # Legítima
    {"valor": 5000.00, "hora": 3, "categoria_cod": 1, "qtd_transacoes_24h": 15},  # Suspeita
    {"valor": 12000.00, "hora": 2, "categoria_cod": 5, "qtd_transacoes_24h": 25}, # Suspeita
    {"valor": 80.00, "hora": 10, "categoria_cod": 3, "qtd_transacoes_24h": 1},    # Legítima
    {"valor": 8500.00, "hora": 23, "categoria_cod": 1, "qtd_transacoes_24h": 18}, # Suspeita
])

predicoes = model.predict(novos_dados)
probabilidades = model.predict_proba(novos_dados)[:, 1]

print("Transação                                          | Predição | Prob. Fraude")
print("-" * 75)
for i, (_, row) in enumerate(novos_dados.iterrows()):
    resultado = "🚨 FRAUDE" if predicoes[i] == 1 else "✅ OK    "
    prob = probabilidades[i] * 100
    print(f"R${row['valor']:>8.2f} | hora:{row['hora']:>2} | cat:{row['categoria_cod']} | txn24h:{row['qtd_transacoes_24h']:>2} | {resultado} | {prob:>5.1f}%")

print("-" * 75)
print(f"\n✅ {sum(predicoes)} transações marcadas como fraude de {len(predicoes)} analisadas")
