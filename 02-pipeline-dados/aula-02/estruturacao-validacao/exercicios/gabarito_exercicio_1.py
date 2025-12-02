"""
Exercício 1: GABARITO
Organizar código em funções
"""

import pandas as pd
import numpy as np


def extrair_dados(caminho):
    """Lê dados de arquivo CSV"""
    df = pd.read_csv(caminho)
    print(f"Extraído: {len(df)} linhas de {caminho}")
    return df


def limpar_dados(df):
    """Remove nulos e duplicatas"""
    antes = len(df)
    df = df.dropna()
    df = df.drop_duplicates()
    depois = len(df)
    print(f"Limpeza: {antes} → {depois} linhas")
    return df


def criar_features(df):
    """Cria features derivadas"""
    df = df.copy()
    df['preco_log'] = np.log1p(df['preco'])
    print("Feature criada: preco_log")
    return df


def salvar_dados(df, caminho):
    """Salva DataFrame em CSV"""
    df.to_csv(caminho, index=False)
    print(f"Salvo em: {caminho}")


def executar_pipeline():
    """Executa pipeline completo"""
    print("="*40)
    print("EXECUTANDO PIPELINE")
    print("="*40)
    
    print("\n1. Extraindo...")
    df = extrair_dados('data/vendas.csv')
    
    print("\n2. Limpando...")
    df = limpar_dados(df)
    
    print("\n3. Criando features...")
    df = criar_features(df)
    
    print("\n4. Salvando...")
    salvar_dados(df, 'data/vendas_processado.csv')
    
    print("\n✅ Pipeline concluído!")


if __name__ == "__main__":
    executar_pipeline()
