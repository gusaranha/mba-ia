"""
Pipeline - Etapa 3: Treinar Modelo
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib


def preparar_dados(df, coluna_target='respondeu_campanha'):
    """
    Separa features (X) e target (y).
    
    Args:
        df: DataFrame completo
        coluna_target: nome da coluna target
        
    Returns:
        X (features), y (target)
    """
    
    # TODO 1: Crie X removendo a coluna target e cliente_id do DataFrame
    # Dica: X = df.drop(columns=[coluna_target, 'cliente_id'])
    
    X = None  # Substitua None pelo código correto
    
    
    # TODO 2: Crie y extraindo apenas a coluna target
    # Dica: y = df[coluna_target]
    
    y = None  # Substitua None pelo código correto
    
    
    return X, y


def dividir_treino_teste(X, y, tamanho_teste=0.2, random_state=42):
    """
    Divide os dados em treino e teste.
    
    Args:
        X: features
        y: target
        tamanho_teste: proporção para teste (0.2 = 20%)
        random_state: semente para reprodutibilidade
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    
    # TODO 3: Use train_test_split para dividir os dados
    # Dica: X_train, X_test, y_train, y_test = train_test_split(
    #           X, y, test_size=tamanho_teste, random_state=random_state
    #       )
    
    X_train, X_test, y_train, y_test = None, None, None, None  # Substitua pelo código
    
    
    # Mostrar tamanhos
    if X_train is not None:
        print(f"Dados de treino: {len(X_train)} registros")
        print(f"Dados de teste: {len(X_test)} registros")
    
    return X_train, X_test, y_train, y_test


def treinar_modelo(X_train, y_train):
    """
    Treina um RandomForestClassifier.
    
    Args:
        X_train: features de treino
        y_train: target de treino
        
    Returns:
        Modelo treinado
    """
    
    print("Treinando modelo...")
    
    # TODO 4: Crie e treine o modelo RandomForestClassifier
    # Passo 1: Criar o modelo
    # Dica: modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    
    modelo = None  # Substitua None pelo código correto
    
    
    # Passo 2: Treinar o modelo (se foi criado)
    # Dica: modelo.fit(X_train, y_train)
    
    if modelo is not None:
        # TODO 5: Treine o modelo usando .fit()
        pass  # Substitua pass pelo código correto
    
    
    print("✅ Modelo treinado!")
    return modelo


def salvar_modelo(modelo, caminho='models/modelo_campanha.pkl'):
    """
    Salva o modelo treinado em disco.
    
    Args:
        modelo: modelo treinado
        caminho: onde salvar
    """
    joblib.dump(modelo, caminho)
    print(f"Modelo salvo em: {caminho}")


# Teste local
if __name__ == "__main__":
    # Carregar dados
    df = pd.read_csv("data/clientes_campanha.csv")
    
    # Preparar
    X, y = preparar_dados(df)
    
    if X is None or y is None:
        print("ERRO: Complete os TODOs 1 e 2!")
    else:
        # Dividir
        X_train, X_test, y_train, y_test = dividir_treino_teste(X, y)
        
        if X_train is None:
            print("ERRO: Complete o TODO 3!")
        else:
            # Treinar
            modelo = treinar_modelo(X_train, y_train)
            
            if modelo is None:
                print("ERRO: Complete os TODOs 4 e 5!")
            else:
                salvar_modelo(modelo)
