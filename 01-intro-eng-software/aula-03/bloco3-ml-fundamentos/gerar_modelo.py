# Interesse apenas para alunos avançados
# bloco3-ml-fundamentos/gerar_modelo.py

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

print("📊 Gerando dataset de transações...")

# Gerar dados sintéticos
np.random.seed(42)

# 70% transações legítimas
n_legitimas = 3500
legitimas = pd.DataFrame({
    'valor': np.random.uniform(10, 200, n_legitimas),
    'hora': np.random.randint(6, 24, n_legitimas),
    'distancia_km': np.random.uniform(0, 50, n_legitimas),
    'transacoes_hoje': np.random.randint(1, 8, n_legitimas),
    'idade_conta_dias': np.random.randint(30, 3650, n_legitimas),
    'fraude': 0
})

# 30% transações fraudulentas
n_fraudes = 1500
fraudes = pd.DataFrame({
    'valor': np.random.uniform(500, 5000, n_fraudes),
    'hora': np.random.randint(0, 6, n_fraudes),
    'distancia_km': np.random.uniform(100, 2000, n_fraudes),
    'transacoes_hoje': np.random.randint(5, 20, n_fraudes),
    'idade_conta_dias': np.random.randint(1, 365, n_fraudes),
    'fraude': 1
})

# Combinar e embaralhar
df = pd.concat([legitimas, fraudes], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"✓ Dataset criado: {len(df)} transações")
print(f"  - Legítimas: {(df['fraude']==0).sum()}")
print(f"  - Fraudes: {(df['fraude']==1).sum()}")

# Separar features e target
X = df.drop('fraude', axis=1)
y = df['fraude']

# Treinar modelo
print("\n🤖 Treinando modelo Random Forest...")
modelo = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
modelo.fit(X, y)

# Avaliar
acuracia = modelo.score(X, y)
print(f"✓ Modelo treinado! Acurácia: {acuracia*100:.1f}%")

# Salvar modelo
print("\n💾 Salvando modelo...")
with open("modelo_fraude.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("✅ Modelo salvo: modelo_fraude.pkl")
print("\n📝 Ordem das features:")
print("  1. valor")
print("  2. hora")
print("  3. distancia_km")
print("  4. transacoes_hoje")
print("  5. idade_conta_dias")