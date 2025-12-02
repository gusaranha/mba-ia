"""
6. PROMOVER MODELO v2.0

Promove o modelo retreinado para produção.
"""
import mlflow
import pickle
import json
from pathlib import Path
from datetime import datetime

print("📦 PROMOVENDO MODELO v2.0")
print("=" * 60)

# Configurar MLflow
mlflow.set_tracking_uri("file:../mlruns")

# Carregar metadata v1.0
metadata_v1_path = Path("../producao/metadata.json")
with open(metadata_v1_path, "r") as f:
    metadata_v1 = json.load(f)

# Buscar melhor modelo do retreino
experiment = mlflow.get_experiment_by_name("deteccao-fraude-retreino-nov-2025")
if experiment is None:
    print("❌ Erro: Execute primeiro '5_retreinar_modelo.py'")
    exit(1)

runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_score DESC"]
)

if len(runs) == 0:
    print("❌ Nenhum experimento de retreino encontrado")
    exit(1)

melhor_run = runs.iloc[0]
run_id = melhor_run["run_id"]
f1_v2 = melhor_run["metrics.f1_score"]
precision_v2 = melhor_run["metrics.precision"]
recall_v2 = melhor_run["metrics.recall"]

print("\n✅ Novo modelo identificado:")
print(f"   Algoritmo: {melhor_run['tags.mlflow.runName']}")
print(f"   F1 Score (treino): {f1_v2:.3f}")
print(f"   Run ID: {run_id[:12]}")

# Comparação
f1_v1 = metadata_v1["f1_score"]
melhoria = ((f1_v2 - f1_v1) / f1_v1) * 100

print(f"\n📊 COMPARAÇÃO v1.0 vs v2.0\n")
print(f"                      v1.0      v2.0    Melhoria")
print(f"   {'─' * 50}")
print(f"   F1 (treino)        {f1_v1:.3f}     {f1_v2:.3f}    {melhoria:+.1f}%")
print(f"   Dados              2000      4000     +100%")
print(f"   Taxa fraude        10%       12.5%    Ajustado")

# Carregar modelo
print(f"\n📥 Carregando modelo do MLflow...")
model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

# Salvar
models_dir = Path("../producao/models")
model_path = models_dir / "producao.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Modelo salvo em: {model_path}")

# Criar metadata v2.0
metadata_v2 = {
    "versao": "v2.0",
    "data_deploy": datetime.now().strftime("%Y-%m-%d"),
    "data_treino": "outubro_novembro_2025",
    "algoritmo": melhor_run['tags.mlflow.runName'],
    "f1_score": float(f1_v2),
    "precision": float(precision_v2),
    "recall": float(recall_v2),
    "run_id": run_id,
    "n_transacoes_treino": 4000,
    "taxa_fraude_treino": 0.125,
    "changelog": [
        "Retreinado com dados Out+Nov (4000 registros)",
        "Taxa de fraude ajustada: 12.5%",
        "Novos padrões incorporados",
        f"Performance: {melhoria:+.1f}% vs v1.0"
    ]
}

metadata_path = Path("../producao/metadata.json")
with open(metadata_path, "w") as f:
    json.dump(metadata_v2, f, indent=2)

print(f"\n✅ Metadata atualizada:")
print(json.dumps(metadata_v2, indent=2))

print(f"\n🚀 Modelo v2.0 pronto para deploy!")
print(f"\n👉 Reinicie a API: 'python ../producao/3_iniciar_api.py'")
