"""
Exercício 2: Filtros e Agregações - GABARITO
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
transacoes_altas = df[df['valor'] > 1000]

print(f"Total: {len(transacoes_altas):,} transações")
print(f"Isso representa {(len(transacoes_altas)/len(df)*100):.2f}% do total")
print()


# ============================================
# TODO 2: Conte quantas transações existem por categoria
# Dica: use df['coluna'].value_counts()
# ============================================

print("TODO 2: Transações por categoria")
print(df['categoria'].value_counts())
print()

# Alternativa com ordenação alfabética:
print("Ordenado alfabeticamente:")
print(df['categoria'].value_counts().sort_index())
print()


# ============================================
# TODO 3: Qual o valor médio das transações fraudulentas?
# Dica: 
#   1. Primeiro filtre: df[df['is_fraud'] == 1]
#   2. Depois calcule média: ['valor'].mean()
# ============================================

print("TODO 3: Valor médio de fraudes")
valor_medio_fraudes = df[df['is_fraud'] == 1]['valor'].mean()
print(f"Valor médio de fraudes: R$ {valor_medio_fraudes:,.2f}")

# Comparação com legítimas:
valor_medio_legitimas = df[df['is_fraud'] == 0]['valor'].mean()
print(f"Valor médio de legítimas: R$ {valor_medio_legitimas:,.2f}")
print(f"Diferença: {(valor_medio_fraudes/valor_medio_legitimas - 1)*100:.1f}% maior")
print()


# ============================================
# TODO 4 (DESAFIO): Qual categoria tem maior proporção de fraudes?
# Dica: use df.groupby('categoria')['is_fraud'].mean()
# Isso calcula a média de is_fraud por categoria (proporção de 1s)
# ============================================

print("TODO 4: Proporção de fraudes por categoria")
proporcao_fraudes = df.groupby('categoria')['is_fraud'].mean()
print(proporcao_fraudes)
print()

# Encontrar a categoria com maior proporção:
categoria_max_fraude = proporcao_fraudes.idxmax()
proporcao_max = proporcao_fraudes.max()
print(f"Categoria com maior proporção de fraudes: {categoria_max_fraude}")
print(f"Proporção: {proporcao_max*100:.2f}%")
print()

print("=" * 50)
print("✅ Exercício 2 concluído!")
print("=" * 50)
