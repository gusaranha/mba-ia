"""
DEMONSTRAÇÃO 1/2 — Classificador de natureza do BO SEM pré-processamento cuidadoso
Disciplina: MLOps & CI/CD — Aula 1

Objetivo didático: mostrar o que acontece quando treinamos um modelo "no piloto
automático", sem tratar valores faltantes, sem tratar outliers e usando Label
Encoding de forma ingênua em uma variável NOMINAL (bairro) — um erro comum.

Compare o resultado deste script com o de
`demo_ml_2_com_preprocessamento.py`, que resolve exatamente esses problemas.

Aviso pedagógico: o dataset (`bos_sinteticos.csv`) tem só 40 linhas e 10
classes — é pequeno demais para conclusões estatísticas robustas. O objetivo
aqui é ilustrar o EFEITO do pré-processamento nas métricas, não avaliar um
modelo real. No projeto de cada aluno, use um volume de dados adequado e
validação cruzada.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.sparse import hstack, csr_matrix
import numpy as np

RANDOM_STATE = 42

# 1) Carregar os dados -------------------------------------------------------
df = pd.read_csv("bos_sinteticos.csv")

# 2) "Pré-processamento" ingênuo ---------------------------------------------
# Valores faltantes: preenchidos com 0 sem pensar no significado (idade 0 não existe!)
df["idade_vitima"] = df["idade_vitima"].fillna(0)

# Outliers: NÃO são tratados — o valor de R$ 480.000 continua no dataset como está.

# Texto: usado "cru", sem lowercase/remover pontuação/remover stopwords
vectorizer = CountVectorizer(lowercase=False)
X_texto = vectorizer.fit_transform(df["texto_relato"])

# Encoding ingênuo: Label Encoding aplicado numa variável NOMINAL (bairro),
# o que faz o modelo enxergar uma ordem que não existe (ex.: Guará=9 > Asa Norte=0)
le_bairro = LabelEncoder()
bairro_enc = le_bairro.fit_transform(df["bairro"]).reshape(-1, 1)

le_turno = LabelEncoder()
turno_enc = le_turno.fit_transform(df["turno"]).reshape(-1, 1)

# Numéricos usados sem nenhuma padronização (escalas muito diferentes: idade ~0-120, prejuízo ~0-480.000)
numericos = df[["valor_prejuizo_reais", "idade_vitima"]].to_numpy()

X = hstack([X_texto, csr_matrix(bairro_enc), csr_matrix(turno_enc), csr_matrix(numericos)])
y = df["natureza"]

# 3) Split treino/teste --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=RANDOM_STATE
)

# 4) Treinar um modelo simples -----------------------------------------------
modelo = DecisionTreeClassifier(random_state=RANDOM_STATE)
modelo.fit(X_train, y_train)

# 5) Avaliar -------------------------------------------------------------
y_pred = modelo.predict(X_test)

acuracia = accuracy_score(y_test, y_pred)
precisao = precision_score(y_test, y_pred, average="weighted", zero_division=0)
revocacao = recall_score(y_test, y_pred, average="weighted", zero_division=0)
f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

print("=" * 60)
print("RESULTADO — SEM pré-processamento cuidadoso")
print("=" * 60)
print(f"Acurácia:  {acuracia:.2%}")
print(f"Precisão:  {precisao:.2%}")
print(f"Revocação: {revocacao:.2%}")
print(f"F1-Score:  {f1:.2%}")
print()
print("Problemas introduzidos de propósito neste script:")
print("- idade_vitima faltante virou 0 (parece um recém-nascido registrando um BO)")
print("- outlier de R$ 480.000 não foi tratado")
print("- 'bairro' (nominal) recebeu Label Encoding, criando uma ordem falsa")
print("- texto não foi normalizado (maiúsculas/minúsculas tratadas como diferentes)")
print("- variáveis numéricas em escalas muito diferentes, sem padronização")
