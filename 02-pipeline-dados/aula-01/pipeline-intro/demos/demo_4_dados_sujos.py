"""
Demo 4: Identificando problemas nos dados
Objetivo: Ver o que pode dar errado
"""

import pandas as pd

# Carregar dados sujos (com problemas propositais)
df = pd.read_csv('../data/transacoes_sujas.csv')

print("=" * 50)
print("DIAGNÓSTICO DO DATASET")
print("=" * 50)
print()

# ===== 1. VERIFICAR VALORES NULOS (NaN/None) =====
print("1. VALORES NULOS POR COLUNA:")
print(df.isnull().sum())
# isnull() = retorna True onde há valor nulo
# sum() = conta quantos True existem em cada coluna
print()

# ===== 2. VERIFICAR DUPLICATAS =====
duplicatas = df.duplicated().sum()
# duplicated() = marca linhas que são cópias exatas de outras
# sum() = conta quantas duplicatas existem
print(f"2. DUPLICATAS: {duplicatas} linhas")
print()

# ===== 3. VERIFICAR VALORES NEGATIVOS =====
negativos = (df['valor'] < 0).sum()
# (df['valor'] < 0) = retorna True onde valor é negativo
# sum() = conta quantos valores negativos existem
print(f"3. VALORES NEGATIVOS: {negativos} transações")
print()
if negativos > 0:
    print("Exemplos:")
    print(df[df['valor'] < 0][['id', 'valor', 'categoria']].head())
    # df[df['valor'] < 0] = filtra apenas linhas com valor negativo
    # [['id', 'valor', 'categoria']] = seleciona apenas essas 3 colunas
    # head() = mostra primeiras 5 linhas
print()

# ===== 4. VERIFICAR CATEGORIAS INVÁLIDAS =====
categorias_validas = ['A', 'B', 'C', 'D']
categorias_invalidas = df[~df['categoria'].isin(categorias_validas)]
# isin(categorias_validas) = retorna True se categoria está na lista válida
# ~ = operador NOT (inverte: pega apenas as INválidas)
# df[...] = filtra apenas linhas com categoria inválida

print(f"4. CATEGORIAS INVÁLIDAS: {len(categorias_invalidas)} transações")
if len(categorias_invalidas) > 0:
    print("Categorias encontradas:")
    print(categorias_invalidas['categoria'].unique())
    # unique() = retorna valores únicos (sem repetição)
print()

# ===== 5. RESUMO GERAL DOS PROBLEMAS =====
print("=" * 50)
print("RESUMO DOS PROBLEMAS")
print("=" * 50)

total_problemas = df.isnull().any(axis=1).sum() + duplicatas + negativos + len(categorias_invalidas)
# any(axis=1) = retorna True se QUALQUER coluna tem nulo naquela linha
# sum() = conta linhas com pelo menos 1 problema
# + duplicatas + negativos + len(categorias_invalidas) = soma todos os problemas

print(f"Total de linhas com problemas: {total_problemas}")
print(f"Linhas limpas: {len(df) - total_problemas}")
print(f"Percentual limpo: {((len(df) - total_problemas) / len(df) * 100):.2f}%")
# len(df) = total de linhas
# .2f = formata com 2 casas decimais