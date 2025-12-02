"""
Demo 6: Treinando primeiro modelo
Objetivo: Ver o processo completo de treinamento
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import time

# Carregar dados limpos
df = pd.read_csv('../data/transacoes_limpas.csv')

print("=" * 50)
print("PREPARAÇÃO DOS DADOS")
print("=" * 50)

# ===== SEPARAR FEATURES (X) E TARGET (Y) =====
# Features (X): variáveis que o modelo usará para prever
# Target (y): variável que queremos prever (is_fraud)

# Converter categoria de texto para número
le = LabelEncoder()
# LabelEncoder = transforma texto em números (A=0, B=1, C=2, D=3)
df['categoria_cod'] = le.fit_transform(df['categoria'])
# fit_transform() = aprende as categorias e converte em uma única etapa

X = df[['valor', 'hora', 'categoria_cod']]
# X = DataFrame com apenas as colunas que serão features
y = df['is_fraud']
# y = Series com apenas a coluna alvo (0 ou 1)

print(f"Features (X): {X.shape[0]} linhas x {X.shape[1]} colunas")
# shape[0] = número de linhas, shape[1] = número de colunas
print(f"Target (y): {y.shape[0]} valores")
print()

print("Primeiras linhas de X:")
print(X.head())
# head() = mostra primeiras 5 linhas
print()

print("Primeiros valores de y:")
print(y.head())
print()

# ===== CRIAR MODELO =====
print("=" * 50)
print("CRIANDO MODELO")
print("=" * 50)
model = RandomForestClassifier(
    n_estimators=100,  # número de árvores de decisão no ensemble
    random_state=42,    # semente para reprodutibilidade (sempre mesmo resultado)
    max_depth=10        # profundidade máxima de cada árvore (evita overfitting)
)
print(model)
# imprime os parâmetros configurados do modelo
print()

# ===== TREINAR MODELO =====
print("=" * 50)
print("TREINANDO MODELO...")
print("=" * 50)
print("(Isso pode levar alguns segundos...)")

inicio = time.time()
# time.time() = retorna timestamp atual em segundos
model.fit(X, y)
# fit() = treina o modelo usando X (features) e y (target)
# o modelo aprende padrões que relacionam X com y
fim = time.time()

print(f"✅ Treinamento concluído em {fim - inicio:.2f} segundos!")
# calcula tempo decorrido e formata com 2 casas decimais
print()

# ===== FAZER PREDIÇÕES =====
print("=" * 50)
print("FAZENDO PREDIÇÕES")
print("=" * 50)
predicoes = model.predict(X)
# predict() = usa o modelo treinado para prever valores
# retorna array com predições (0 ou 1) para cada linha de X

print("Primeiras 10 predições:")
print(predicoes[:10])
# [:10] = slice dos primeiros 10 elementos
print()

print("Primeiros 10 valores reais:")
print(y.values[:10])
# .values = converte Series para array numpy
print()

# ===== COMPARAR PREDIÇÕES COM VALORES REAIS =====
acertos = (predicoes == y).sum()
# (predicoes == y) = cria array booleano (True onde acertou)
# sum() = conta quantos True existem
total = len(y)
# len(y) = quantidade total de exemplos
print(f"Acertou {acertos} de {total} transações")
print(f"Acurácia: {(acertos/total)*100:.2f}%")
# (acertos/total)*100 = percentual de acertos
print()

print("⚠️  ATENÇÃO: Testamos nos mesmos dados que treinamos!")
print("Isso NÃO é a forma correta. Veremos na próxima etapa.")
# treinar e testar nos mesmos dados gera overfitting (decorar ao invés de aprender)