import pandas as pd
import pickle
import numpy as np

# Carregar modelo
with open('modelo_fraude.pkl', 'rb') as f:
    model = pickle.load(f)

# Ler dados de produção
df = pd.read_csv('dados_producao.csv')

print(f"Processando {len(df)} transações...")

# Preparar dados (mesmo código do notebook)
# Manter apenas as colunas que o modelo conhece
colunas_modelo = ['id', 'valor', 'hora', 'categoria']
X = df[colunas_modelo]

# Converter categoria para número
categoria_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
X['categoria'] = X['categoria'].map(categoria_map)

# Fazer predições
predicoes = model.predict(X)

# Resultados
fraudes_detectadas = predicoes.sum()
verdadeiras_fraudes = df['is_fraud'].sum()

print(f"\n{'='*50}")
print(f"RESULTADOS DO PRIMEIRO DIA EM PRODUÇÃO")
print(f"{'='*50}")
print(f"Total de transações: {len(df)}")
print(f"Fraudes detectadas pelo modelo: {fraudes_detectadas}")
print(f"Fraudes reais: {verdadeiras_fraudes}")
print(f"\nFalsos positivos: {fraudes_detectadas - verdadeiras_fraudes}")
print(f"Taxa de falso positivo: {((fraudes_detectadas - verdadeiras_fraudes) / len(df) * 100):.1f}%")
