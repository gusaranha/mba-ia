import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
import pickle

print("Carregando dados de treino...")
df = pd.read_csv('dados_treino.csv')

# Limpeza
df = df.dropna()
df = df.drop_duplicates()

# Preparar features
X = df.drop('is_fraud', axis=1)
y = df['is_fraud']

# Converter categoria para número
categoria_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
X['categoria'] = X['categoria'].map(categoria_map)

# Dividir treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Treinar modelo
print("Treinando modelo...")
model = RandomForestClassifier(n_estimators=20, max_depth=8, random_state=42)
model.fit(X_train, y_train)

# Avaliar
y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred)

print(f"\n{'='*50}")
print("RESULTADOS DO MODELO")
print(f"{'='*50}")
print(f"F1 Score: {f1:.4f}")
print(f"\n{classification_report(y_test, y_pred)}")

# Salvar modelo
with open('modelo_fraude.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ Modelo salvo em modelo_fraude.pkl")
