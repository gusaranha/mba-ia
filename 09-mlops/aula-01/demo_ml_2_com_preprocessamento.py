"""
DEMONSTRAÇÃO 2/2 — Classificador de natureza do BO COM pré-processamento
Disciplina: MLOps & CI/CD — Aula 1

Objetivo didático: mesma tarefa e mesmo modelo do script 1
(`demo_ml_1_sem_preprocessamento.py`), mas agora tratando corretamente:
valores faltantes, outliers, encoding (Label x One-Hot) e normalização de
texto e de escala numérica. Compare as métricas impressas ao final dos dois
scripts.

Aviso pedagógico: o dataset (`bos_sinteticos.csv`) tem só 40 linhas e 10
classes — pequeno demais para conclusões estatísticas robustas. O objetivo é
ilustrar o EFEITO do pré-processamento, não avaliar um modelo real.
"""
import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.sparse import hstack, csr_matrix

RANDOM_STATE = 42

# lista curta de stopwords em portugues (sem depender de pacotes externos/internet)
STOPWORDS_PT = {
    "a", "o", "e", "de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos",
    "que", "com", "sem", "por", "para", "um", "uma", "seu", "sua", "foi", "ter",
    "apos", "se", "ao", "as", "os",
}


def limpar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-zà-ú0-9\s]", " ", texto)
    palavras = [p for p in texto.split() if p not in STOPWORDS_PT]
    return " ".join(palavras)


# 1) Carregar os dados -------------------------------------------------------
df = pd.read_csv("bos_sinteticos.csv")

# 2) Tratar valores faltantes -------------------------------------------
# idade_vitima: imputar com a MEDIANA (mais robusta a outliers que a média),
# e criar uma coluna indicando que o valor foi imputado (boa prática de MLOps:
# preserva a informação de que aquele dado não veio do comunicante).
df["idade_vitima_faltante"] = df["idade_vitima"].isna().astype(int)
mediana_idade = df["idade_vitima"].median()
df["idade_vitima"] = df["idade_vitima"].fillna(mediana_idade)

# 3) Tratar outliers -------------------------------------------------------
# valor_prejuizo_reais: usar o metodo do IQR (intervalo interquartil) para
# limitar (winsorizar) valores extremos, em vez de deixar um unico registro
# dominar a escala da variavel.
q1, q3 = df["valor_prejuizo_reais"].quantile([0.25, 0.75])
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr
df["valor_prejuizo_reais"] = df["valor_prejuizo_reais"].clip(upper=limite_superior)

# idade_vitima: valores fora de uma faixa plausivel (ex.: 0-100) sao outliers
# quase certamente por erro de digitacao -> limitar a faixa plausivel.
df["idade_vitima"] = df["idade_vitima"].clip(lower=10, upper=100)

# 4) Texto limpo antes do TF-IDF ------------------------------------------
df["texto_limpo"] = df["texto_relato"].apply(limpar_texto)
vectorizer = TfidfVectorizer()
X_texto = vectorizer.fit_transform(df["texto_limpo"])

# 5) Encoding correto por tipo de variável --------------------------------
# turno é ORDINAL (Madrugada < Manhã < Tarde < Noite em termos de sequência do
# dia) -> Label Encoding com ordem explícita.
ordem_turno = ["Madrugada", "Manhã", "Tarde", "Noite"]
turno_enc = df["turno"].apply(lambda x: ordem_turno.index(x)).to_numpy().reshape(-1, 1)

# bairro é NOMINAL (sem ordem) -> One-Hot Encoding, para não inventar uma
# relação de grandeza que não existe entre os bairros.
ohe = OneHotEncoder(sparse_output=True, handle_unknown="ignore")
bairro_ohe = ohe.fit_transform(df[["bairro"]])

# booleanos já são 0/1 -> não precisam de encoding adicional
booleanos = df[["houve_violencia", "reincidencia"]].astype(int).to_numpy()

# 6) Padronizar variáveis numéricas (escalas comparáveis) -------------------
scaler = StandardScaler()
numericos = scaler.fit_transform(df[["valor_prejuizo_reais", "idade_vitima"]])

X = hstack([
    X_texto,
    csr_matrix(bairro_ohe),
    csr_matrix(turno_enc),
    csr_matrix(booleanos),
    csr_matrix(numericos),
    csr_matrix(df[["idade_vitima_faltante"]].to_numpy()),
])
y = df["natureza"]

# 7) Split treino/teste ----------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=RANDOM_STATE
)

# 8) Treinar o MESMO tipo de modelo do script 1, para comparação justa ------
modelo = DecisionTreeClassifier(random_state=RANDOM_STATE)
modelo.fit(X_train, y_train)

# 9) Avaliar ----------------------------------------------------------------
y_pred = modelo.predict(X_test)

acuracia = accuracy_score(y_test, y_pred)
precisao = precision_score(y_test, y_pred, average="weighted", zero_division=0)
revocacao = recall_score(y_test, y_pred, average="weighted", zero_division=0)
f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

print("=" * 60)
print("RESULTADO — COM pré-processamento")
print("=" * 60)
print(f"Acurácia:  {acuracia:.2%}")
print(f"Precisão:  {precisao:.2%}")
print(f"Revocação: {revocacao:.2%}")
print(f"F1-Score:  {f1:.2%}")
print()
print("O que foi corrigido em relação ao script 1:")
print("- idade_vitima faltante: imputada com a mediana + flag indicando imputação")
print("- outlier de prejuízo: limitado (clip) pelo método do IQR")
print("- idade fora da faixa plausível: limitada a 10-100 anos")
print("- 'bairro' (nominal) → One-Hot Encoding | 'turno' (ordinal) → Label Encoding com ordem certa")
print("- texto normalizado (minúsculas, sem pontuação, sem stopwords) antes do TF-IDF")
print("- variáveis numéricas padronizadas (StandardScaler) antes do treino")
