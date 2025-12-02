"""
Demo 7: Validação correta do modelo
Objetivo: Avaliar performance em dados não vistos
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Carregar dados
df = pd.read_csv('../data/transacoes_limpas.csv')

# Preparar features
le = LabelEncoder()
# LabelEncoder() = cria um objeto que vai fazer a conversão texto → número

df['categoria_cod'] = le.fit_transform(df['categoria'])
# fit_transform() faz 2 coisas:
#   1. fit() = aprende quais categorias existem ('A', 'B', 'C', 'D')
#   2. transform() = converte cada categoria para número

# RESULTADO:
# 'A' → 0
# 'B' → 1
# 'C' → 2
# 'D' → 3

X = df[['valor', 'hora', 'categoria_cod']]
y = df['is_fraud']

print("=" * 50)
print("DIVIDINDO DADOS")
print("=" * 50)

# ===== DIVIDIR DADOS EM TREINO E TESTE =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,      # 30% dos dados vão para teste (70% para treino)
    random_state=42,    # semente para sempre gerar a mesma divisão
    stratify=y          # mantém a proporção de fraudes igual em treino e teste
)
# train_test_split() = divide dados aleatoriamente
# retorna 4 conjuntos: X_train, X_test, y_train, y_test

print(f"Treino: {len(X_train):,} transações")
# :, = formatador que adiciona separador de milhares
print(f"Teste:  {len(X_test):,} transações")
print()
print(f"Fraudes no treino: {y_train.sum():,} ({y_train.mean()*100:.2f}%)")
# sum() = conta quantas fraudes (1's)
# mean() = média (proporção de 1's)
print(f"Fraudes no teste:  {y_test.sum():,} ({y_test.mean()*100:.2f}%)")
print()

# ===== TREINAR MODELO =====
print("=" * 50)
print("TREINANDO MODELO")
print("=" * 50)

model = RandomForestClassifier(
    n_estimators=100,  # 100 árvores de decisão
    max_depth=10,      # profundidade máxima de cada árvore
    random_state=42    # reprodutibilidade
)

print("Treinando...")
model.fit(X_train, y_train)
# fit() = treina SOMENTE com dados de treino
# modelo NÃO vê os dados de teste durante o treinamento
print("✅ Treinamento concluído!")
print()

# ===== FAZER PREDIÇÕES =====
print("=" * 50)
print("FAZENDO PREDIÇÕES NO CONJUNTO DE TESTE")
print("=" * 50)

y_pred = model.predict(X_test)
# predict() = faz predições nos dados de TESTE (não vistos no treino)
# retorna array com 0 (legítima) ou 1 (fraude) para cada transação

print(f"Predições realizadas: {len(y_pred):,}")
print()

# ===== CALCULAR MÉTRICAS =====
print("=" * 50)
print("MÉTRICAS DE PERFORMANCE")
print("=" * 50)

accuracy = accuracy_score(y_test, y_pred)
# accuracy = (acertos totais) / (total de predições)
# % de predições corretas (legítimas + fraudes)

precision = precision_score(y_test, y_pred)
# precision = (verdadeiros positivos) / (verdadeiros positivos + falsos positivos)
# das transações que marcamos como fraude, quantas % REALMENTE eram fraude?

recall = recall_score(y_test, y_pred)
# recall = (verdadeiros positivos) / (verdadeiros positivos + falsos negativos)
# das fraudes reais, quantas % conseguimos detectar?

f1 = f1_score(y_test, y_pred)
# f1 = média harmônica entre precision e recall
# balanceia precision e recall em uma única métrica

print(f"Acurácia:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Precisão:  {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
print(f"F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
# :.4f = 4 casas decimais
print()

# ===== MATRIZ DE CONFUSÃO =====
print("=" * 50)
print("MATRIZ DE CONFUSÃO")
print("=" * 50)

cm = confusion_matrix(y_test, y_pred)
# confusion_matrix() = matriz 2x2 que mostra acertos e erros
# cm[0][0] = verdadeiros negativos (legítima prevista como legítima)
# cm[0][1] = falsos positivos (legítima prevista como fraude)
# cm[1][0] = falsos negativos (fraude prevista como legítima)
# cm[1][1] = verdadeiros positivos (fraude prevista como fraude)

print("\n                Predito")
print("               Legít  Fraude")
print(f"Real Legít   {cm[0][0]:7d} {cm[0][1]:7d}")
# :7d = inteiro com 7 espaços (alinhamento)
print(f"     Fraude  {cm[1][0]:7d} {cm[1][1]:7d}")
print()

# ===== INTERPRETAR MATRIZ =====
vn, fp = cm[0]  # linha 0: verdadeiros negativos, falsos positivos
fn, vp = cm[1]  # linha 1: falsos negativos, verdadeiros positivos

print("Interpretação:")
print(f"  ✅ Verdadeiros Negativos: {vn:,} (legítimas identificadas corretamente)")
print(f"  ✅ Verdadeiros Positivos: {vp:,} (fraudes detectadas)")
print(f"  ❌ Falsos Positivos: {fp:,} (legítimas marcadas como fraude)")
# ERRO TIPO 1: alarme falso - bloqueia cliente legítimo
print(f"  ❌ Falsos Negativos: {fn:,} (fraudes que passaram despercebidas)")
# ERRO TIPO 2: fraude não detectada - prejuízo financeiro
print()

# ===== RELATÓRIO DETALHADO =====
print("=" * 50)
print("RELATÓRIO DETALHADO")
print("=" * 50)
print(classification_report(y_test, y_pred, target_names=['Legítima', 'Fraude']))
# classification_report() = gera relatório completo com:
# - precision, recall, f1-score para cada classe
# - support = quantidade de exemplos de cada classe
# - macro avg = média simples entre as classes
# - weighted avg = média ponderada pelo número de exemplos