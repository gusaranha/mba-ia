"""
Demo 5: Aplicando limpezas progressivas
Objetivo: Transformar dados sujos em dados limpos
"""

import pandas as pd

print("Carregando dados sujos...")
df = pd.read_csv('../data/transacoes_sujas.csv')
print(f"Linhas iniciais: {len(df)}")
# len(df) = conta o número total de linhas no DataFrame
print()

# ===== PASSO 1: REMOVER VALORES NULOS =====
print("PASSO 1: Removendo valores nulos...")
antes = len(df)
df = df.dropna()
# dropna() = remove TODAS as linhas que têm pelo menos 1 valor nulo
depois = len(df)
print(f"  Removidas: {antes - depois} linhas")
print(f"  Restantes: {depois}")
print()

# ===== PASSO 2: REMOVER DUPLICATAS =====
print("PASSO 2: Removendo duplicatas...")
antes = len(df)
df = df.drop_duplicates()
# drop_duplicates() = remove linhas que são cópias exatas de outras
# mantém apenas a primeira ocorrência
depois = len(df)
print(f"  Removidas: {antes - depois} linhas")
print(f"  Restantes: {depois}")
print()

# ===== PASSO 3: REMOVER VALORES NEGATIVOS =====
print("PASSO 3: Removendo valores negativos...")
antes = len(df)
df = df[df['valor'] > 0]
# df['valor'] > 0 = cria máscara booleana (True onde valor é positivo)
# df[...] = filtra, mantendo apenas linhas onde a condição é True
depois = len(df)
print(f"  Removidas: {antes - depois} linhas")
print(f"  Restantes: {depois}")
print()

# ===== PASSO 4: MANTER APENAS CATEGORIAS VÁLIDAS =====
print("PASSO 4: Removendo categorias inválidas...")
antes = len(df)
categorias_validas = ['A', 'B', 'C', 'D']
df = df[df['categoria'].isin(categorias_validas)]
# isin(categorias_validas) = retorna True se categoria está na lista válida
# df[...] = mantém apenas linhas com categorias válidas
depois = len(df)
print(f"  Removidas: {antes - depois} linhas")
print(f"  Restantes: {depois}")
print()

# ===== PASSO 5: RESETAR ÍNDICES =====
df = df.reset_index(drop=True)
# reset_index() = recria índices de 0 a n-1 (sequencial)
# drop=True = descarta o índice antigo (não cria coluna extra)

# ===== SALVAR DADOS LIMPOS =====
print("=" * 50)
print("LIMPEZA CONCLUÍDA!")
print("=" * 50)
print(f"Linhas finais: {len(df)}")
print(f"Redução: {((500000 - len(df)) / 500000 * 100):.2f}%")
# calcula percentual de dados removidos em relação ao total original
# .2f = formata com 2 casas decimais
print()

df.to_csv('../data/transacoes_limpas.csv', index=False)
# to_csv() = salva DataFrame em arquivo CSV
# index=False = não salva a coluna de índice no arquivo
print("✅ Dados limpos salvos em '../data/transacoes_limpas.csv'")
print()

# ===== VERIFICAÇÃO FINAL =====
print("Verificação final:")
print(f"  Nulos: {df.isnull().sum().sum()}")
# primeiro sum() = soma nulos por coluna
# segundo sum() = soma total de todos os nulos

print(f"  Duplicatas: {df.duplicated().sum()}")
# verifica se ainda há duplicatas (deve ser 0)

print(f"  Valores negativos: {(df['valor'] < 0).sum()}")
# verifica se ainda há valores negativos (deve ser 0)

print(f"  Categorias inválidas: {(~df['categoria'].isin(categorias_validas)).sum()}")
# ~ = operador NOT, inverte para pegar inválidas
# deve ser 0 (nenhuma categoria inválida)