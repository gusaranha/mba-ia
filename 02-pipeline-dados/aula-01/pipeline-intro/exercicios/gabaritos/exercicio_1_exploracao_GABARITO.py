"""
Exercício 1: Exploração Básica de Dados - GABARITO
Objetivo: Familiarizar-se com comandos básicos do Pandas
"""
import pandas as pd

# Dataset já carregado
df = pd.read_csv('../data/transacoes.csv')

print("=" * 50)
print("EXERCÍCIO 1: EXPLORAÇÃO BÁSICA")
print("=" * 50)
print()

# ============================================
# TODO 1: Mostre as primeiras 10 linhas
# Dica: use df.head(n) onde n é o número de linhas
# ============================================

print("TODO 1: Primeiras 10 linhas")
print(df.head(10))
print()

# ============================================
# TODO 2: Quantas transações existem no total?
# Dica: use df.shape para ver dimensões (linhas, colunas)
# ============================================

print("TODO 2: Total de transações")
total = df.shape[0]
print(f"Total de transações: {total:,}")
print()

# ============================================
# TODO 3: Quantas colunas o dataset tem?
# Dica: df.shape retorna (linhas, colunas)
# ============================================

print("TODO 3: Número de colunas")
num_colunas = df.shape[1]
print(f"Número de colunas: {num_colunas}")
print()

# ============================================
# TODO 4 (DESAFIO): Qual é o valor máximo de transação?
# Dica: use df['coluna'].max()
# ============================================

print("TODO 4: Valor máximo")
valor_max = df['valor'].max()
print(f"Valor máximo: R$ {valor_max:,.2f}")
print()

print("=" * 50)
print("✅ Exercício 1 concluído!")
print("=" * 50)
