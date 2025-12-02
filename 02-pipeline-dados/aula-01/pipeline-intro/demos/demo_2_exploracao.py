"""
Demo 2: Explorando o dataset de transações
Objetivo: Conhecer os dados antes de qualquer processamento
"""

import pandas as pd

df = pd.read_csv('../data/transacoes.csv')

# Dimensões do dataset
print("=" * 50)
print("DIMENSÕES")
print("=" * 50)
print(f"Linhas (transações): {df.shape[0]:,}")
print(f"Colunas (características): {df.shape[1]}")
print()

# Estatísticas das colunas numéricas
print("=" * 50)
print("ESTATÍSTICAS")
print("=" * 50)
print(df.describe())
print()

# Distribuição de fraudes
print("=" * 50)
print("DISTRIBUIÇÃO DE FRAUDES")
print("=" * 50)
print(df['is_fraud'].value_counts())
print()
print("Proporção:")
print(df['is_fraud'].value_counts(normalize=True))
print()

# Distribuição por categoria
print("=" * 50)
print("DISTRIBUIÇÃO POR CATEGORIA")
print("=" * 50)
print(df['categoria'].value_counts())
print()

# Valores por categoria
print("=" * 50)
print("VALOR MÉDIO POR CATEGORIA")
print("=" * 50)
print(df.groupby('categoria')['valor'].mean())
