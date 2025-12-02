"""
Demo 1: Carregando dados de transações
Objetivo: Ler arquivo CSV e entender a estrutura básica
"""

import pandas as pd

# Carregar dados do CSV
df = pd.read_csv('../data/transacoes.csv')

# O que é df?
print("Tipo da variável df:")
print(type(df))
print()

# Mostrar primeiras linhas
print("Primeiras 5 transações:")
print(df.head())
print()

# Informações básicas
print("Informações gerais:")
print(df.info())
