"""
Exercício 3: Limpeza de Dados - GABARITO
Objetivo: Identificar e corrigir problemas nos dados
"""
import pandas as pd

df = pd.read_csv('../data/transacoes_sujas.csv')

print("=" * 50)
print("EXERCÍCIO 3: LIMPEZA DE DADOS")
print("=" * 50)
print()

print(f"Linhas iniciais: {len(df):,}")
print()

# ============================================
# TODO 1: Quantos valores nulos existem em cada coluna?
# Dica: use df.isnull().sum()
# ============================================

print("TODO 1: Valores nulos por coluna")
nulos = df.isnull().sum()
print(nulos)
print()

# Informação adicional:
total_nulos = df.isnull().sum().sum()
print(f"Total de valores nulos no dataset: {total_nulos}")
print()


# ============================================
# TODO 2: Remova as linhas com valores nulos
# Dica: df = df.dropna()
# Lembre-se de reatribuir ao df!
# ============================================

print("TODO 2: Removendo valores nulos...")
linhas_antes = len(df)
df = df.dropna()
linhas_removidas = linhas_antes - len(df)

print(f"Linhas removidas: {linhas_removidas}")
print(f"Linhas após remover nulos: {len(df):,}")
print()


# ============================================
# TODO 3: Remova transações com valor negativo
# Dica: df = df[df['valor'] > 0]
# ============================================

print("TODO 3: Removendo valores negativos...")
linhas_antes = len(df)
df = df[df['valor'] > 0]
linhas_removidas = linhas_antes - len(df)

print(f"Linhas removidas: {linhas_removidas}")
print(f"Linhas após remover negativos: {len(df):,}")
print()


# ============================================
# TODO 4 (DESAFIO): Salve o dataset limpo em um novo arquivo
# Dica: df.to_csv('nome_arquivo.csv', index=False)
# Salve como 'transacoes_limpas_exercicio.csv'
# ============================================

print("TODO 4: Salvando dataset limpo...")
df.to_csv('../data/transacoes_limpas_exercicio.csv', index=False)
print("✅ Dataset salvo em '../data/transacoes_limpas_exercicio.csv'")
print()

# Verificações finais:
print("=" * 50)
print("VERIFICAÇÕES FINAIS")
print("=" * 50)
print(f"Total de linhas no dataset limpo: {len(df):,}")
print(f"Valores nulos restantes: {df.isnull().sum().sum()}")
print(f"Valores negativos restantes: {(df['valor'] < 0).sum()}")
print()

print("=" * 50)
print("✅ Exercício 3 concluído!")
print("=" * 50)
print()
print("Verifique se o arquivo foi criado:")
print("  ../data/transacoes_limpas_exercicio.csv")
