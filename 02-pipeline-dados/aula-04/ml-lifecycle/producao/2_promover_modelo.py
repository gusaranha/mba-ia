"""
2. PROMOVER MODELO PARA PRODUÇÃO

Busca o melhor modelo do MLflow e promove para produção.
"""
import mlflow
import pickle
import json
from pathlib import Path
from datetime import datetime

print("📦 PROMOVENDO MODELO PARA PRODUÇÃO")
print("=" * 60)

# Configurar MLflow
mlflow.set_tracking_uri("file:../mlruns")

# Buscar melhor modelo
experiment = mlflow.get_experiment_by_name("deteccao-fraude-outubro-2025")
if experiment is None:
    print("❌ Erro: Execute primeiro '1_rodar_experimentos.py'")
    exit(1)

runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_score DESC"]
)

if len(runs) == 0:
    print("❌ Nenhum experimento encontrado")
    exit(1)

melhor_run = runs.iloc[0]
run_id = melhor_run["run_id"]
f1 = melhor_run["metrics.f1_score"]
precision = melhor_run["metrics.precision"]
recall = melhor_run["metrics.recall"]

print("\n✅ Melhor modelo identificado:")
print(f"   Algoritmo: {melhor_run['tags.mlflow.runName']}")
print(f"   F1 Score: {f1:.3f}")
print(f"   Precision: {precision:.3f}")
print(f"   Recall: {recall:.3f}")
print(f"   Run ID: {run_id[:12]}")

# Carregar modelo do MLflow
print("\n📥 Carregando modelo do MLflow...")
model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

# Criar diretório models se não existir
models_dir = Path("../producao/models")
models_dir.mkdir(parents=True, exist_ok=True)

# Salvar modelo em produção
model_path = models_dir / "producao.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Modelo salvo em: {model_path}")

# Criar metadata
metadata = {
    "versao": "v1.0",
    "data_deploy": datetime.now().strftime("%Y-%m-%d"),
    "data_treino": "outubro_2025",
    "algoritmo": melhor_run['tags.mlflow.runName'],
    "f1_score": float(f1),
    "precision": float(precision),
    "recall": float(recall),
    "run_id": run_id,
    "n_transacoes_treino": 2000,
    "taxa_fraude_treino": 0.10
}

metadata_path = Path("../producao/metadata.json")
with open(metadata_path, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"\n✅ Metadata atualizada:")
print(json.dumps(metadata, indent=2))

print(f"\n🚀 Modelo v1.0 pronto para produção!")
print(f"\n👉 Próximo passo: Execute '../producao/3_iniciar_api.py'")
