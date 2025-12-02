"""
Demo 6B: Exemplos de predição do modelo
Objetivo: Ver o modelo prevendo transações específicas
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Carregar e preparar dados
df = pd.read_csv('../data/transacoes_limpas.csv')
le = LabelEncoder()
df['categoria_cod'] = le.fit_transform(df['categoria'])

X = df[['valor', 'hora', 'categoria_cod']]
y = df['is_fraud']

# Treinar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X, y)

print("=" * 50)
print("EXEMPLOS DE PREDIÇÕES")
print("=" * 50)
print()

# ===== EXEMPLO 1: PEGAR TRANSAÇÕES REAIS DO DATASET =====
print("1. TRANSAÇÕES REAIS DO DATASET:")
print("-" * 50)

# Pegar 5 transações aleatórias
exemplos = df.sample(5, random_state=42)

for idx, row in exemplos.iterrows():
    # Preparar features para predição
    features = [[row['valor'], row['hora'], row['categoria_cod']]]
    
    # Fazer predição
    predicao = model.predict(features)[0]
    probabilidade = model.predict_proba(features)[0]
    
    print(f"Transação ID {row['id']}:")
    print(f"  Valor: R$ {row['valor']:.2f}")
    print(f"  Hora: {row['hora']}h")
    print(f"  Categoria: {row['categoria']}")
    print(f"  Real: {'FRAUDE' if row['is_fraud'] == 1 else 'LEGÍTIMA'}")
    print(f"  Predição: {'FRAUDE' if predicao == 1 else 'LEGÍTIMA'}")
    print(f"  Probabilidade Fraude: {probabilidade[1]*100:.1f}%")
    print(f"  Status: {'✅ ACERTOU' if predicao == row['is_fraud'] else '❌ ERROU'}")
    print()

# ===== EXEMPLO 2: CRIAR TRANSAÇÕES FICTÍCIAS =====
print("=" * 50)
print("2. TRANSAÇÕES FICTÍCIAS (CRIADAS MANUALMENTE):")
print("-" * 50)
print()

# Criar transações de teste
transacoes_teste = [
    {'valor': 50.0, 'hora': 14, 'categoria': 'A', 'descricao': 'Compra pequena, horário comercial'},
    {'valor': 15000.0, 'hora': 3, 'categoria': 'B', 'descricao': 'Valor alto, madrugada'},
    {'valor': 200.0, 'hora': 18, 'categoria': 'C', 'descricao': 'Valor médio, fim da tarde'},
    {'valor': 45000.0, 'hora': 23, 'categoria': 'D', 'descricao': 'Valor muito alto, noite'},
]

for i, trans in enumerate(transacoes_teste, 1):
    # Converter categoria para código
    categoria_cod = le.transform([trans['categoria']])[0]
    
    # Preparar features
    features = [[trans['valor'], trans['hora'], categoria_cod]]
    
    # Fazer predição
    predicao = model.predict(features)[0]
    probabilidade = model.predict_proba(features)[0]
    
    print(f"Teste {i}: {trans['descricao']}")
    print(f"  Valor: R$ {trans['valor']:.2f}")
    print(f"  Hora: {trans['hora']}h")
    print(f"  Categoria: {trans['categoria']}")
    print(f"  Predição: {'🚨 FRAUDE' if predicao == 1 else '✅ LEGÍTIMA'}")
    print(f"  Confiança: {max(probabilidade)*100:.1f}%")
    print(f"  Prob. Fraude: {probabilidade[1]*100:.1f}%")
    print()