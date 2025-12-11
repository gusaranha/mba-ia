"""
Script SIMPLIFICADO de treinamento do modelo de detecção de fraude.

Este script carrega o dataset CSV já gerado e treina o modelo.

Uso:
    python train_model_simple.py

Requisitos:
    - fraud_dataset.csv no mesmo diretório
    - scikit-learn instalado
"""

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


def main():
    print("\n" + "=" * 70)
    print("TREINAMENTO SIMPLIFICADO - MODELO DE DETECÇÃO DE FRAUDE")
    print("=" * 70)
    
    # 1. Carregar dataset
    print("\n📂 Carregando dataset...")
    df = pd.read_csv('fraud_dataset.csv')
    print(f"✅ Dataset carregado: {len(df)} transações")
    print(f"   - Legítimas: {(df['Class']==0).sum()}")
    print(f"   - Fraudulentas: {(df['Class']==1).sum()}")
    
    # 2. Preparar dados
    print("\n🔀 Preparando dados...")
    feature_names = ['Time'] + [f'V{i}' for i in range(1, 11)] + ['Amount']
    X = df[feature_names].values
    y = df['Class'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Treino: {len(X_train)} | Teste: {len(X_test)}")
    
    # 3. Treinar modelo
    print("\n⏳ Treinando modelo Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("✅ Modelo treinado!")
    
    # 4. Avaliar
    print("\n📊 Avaliando modelo...")
    y_pred = model.predict(X_test)
    
    print("\nMatriz de Confusão:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  VN: {cm[0][0]}  |  FP: {cm[0][1]}")
    print(f"  FN: {cm[1][0]}  |  VP: {cm[1][1]}")
    
    print("\nMétricas:")
    print(classification_report(y_test, y_pred, 
                                target_names=['Legítima', 'Fraudulenta']))
    
    # 5. Salvar modelo
    print("💾 Salvando modelo...")
    with open('fraud_detection_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("✅ Modelo salvo: fraud_detection_model.pkl")
    
    print("\n" + "=" * 70)
    print("✅ CONCLUÍDO!")
    print("=" * 70)
    print("\n📦 Próximo passo: python test_fraud_model.py\n")


if __name__ == "__main__":
    main()
