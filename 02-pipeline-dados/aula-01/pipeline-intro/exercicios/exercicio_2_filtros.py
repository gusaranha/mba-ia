"""
Exercício 2: Filtros e Agregações
Objetivo: Aprender a filtrar e agrupar dados
"""

import pandas as pd

df = pd.read_csv('../data/transacoes.csv')

print("=" * 50)
print("EXERCÍCIO 2: FILTROS E AGREGAÇÕES")
print("=" * 50)
print()

# ============================================
# TODO 1: Filtre apenas transações com valor acima de R$ 1000
# Dica: df[df['coluna'] > valor]
# ============================================

print("TODO 1: Transações acima de R$ 1000")
# Seu código aqui
# transacoes_altas = 

# print(f"Total: {len(transacoes_altas)}")
print()


# ============================================
# TODO 2: Conte quantas transações existem por categoria
# Dica: use df['coluna'].value_counts()
# ============================================

print("TODO 2: Transações por categoria")
# Seu código aqui


print()

# ============================================
# TODO 3: Qual o valor médio das transações fraudulentas?
# Dica: 
#   1. Primeiro filtre: df[df['is_fraud'] == 1]
#   2. Depois calcule média: ['valor'].mean()
# ============================================

print("TODO 3: Valor médio de fraudes")
# Seu código aqui
# valor_medio_fraudes = 


print()

# ============================================
# TODO 4 (DESAFIO): Qual categoria tem maior proporção de fraudes?
# Dica: use df.groupby('categoria')['is_fraud'].mean()
# Isso calcula a média de is_fraud por categoria (proporção de 1s)
# ============================================

print("TODO 4: Proporção de fraudes por categoria")
# Seu código aqui


print()
