"""
Exercício 3: Limpeza de Dados
Objetivo: Identificar e corrigir problemas nos dados
"""

import pandas as pd

df = pd.read_csv('../data/transacoes_sujas.csv')

print("=" * 50)
print("EXERCÍCIO 3: LIMPEZA DE DADOS")
print("=" * 50)
print()

print(f"Linhas iniciais: {len(df)}")
print()

# ============================================
# TODO 1: Quantos valores nulos existem em cada coluna?
# Dica: use df.isnull().sum()
# ============================================

print("TODO 1: Valores nulos por coluna")
# Seu código aqui


print()

# ============================================
# TODO 2: Remova as linhas com valores nulos
# Dica: df = df.dropna()
# Lembre-se de reatribuir ao df!
# ============================================

print("TODO 2: Removendo valores nulos...")
# Seu código aqui


print(f"Linhas após remover nulos: {len(df)}")
print()


# ============================================
# TODO 3: Remova transações com valor negativo
# Dica: df = df[df['valor'] > 0]
# ============================================

print("TODO 3: Removendo valores negativos...")
# Seu código aqui


print(f"Linhas após remover negativos: {len(df)}")
print()


# ============================================
# TODO 4 (DESAFIO): Salve o dataset limpo em um novo arquivo
# Dica: df.to_csv('nome_arquivo.csv', index=False)
# Salve como 'transacoes_limpas_exercicio.csv'
# ============================================

print("TODO 4: Salvando dataset limpo...")
# Seu código aqui


print()
