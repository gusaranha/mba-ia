"""
Módulo de transformação de dados
"""

import pandas as pd
import numpy as np


def limpar_dados(df):
    """
    Remove valores nulos e duplicatas.
    
    Args:
        df: DataFrame a ser limpo
        
    Returns:
        DataFrame limpo
    """
    antes = len(df)
    df = df.dropna()
    df = df.drop_duplicates()
    depois = len(df)
    print(f"  Limpeza: {antes} → {depois} linhas")
    return df


def criar_features(df):
    """
    Cria features derivadas.
    
    Args:
        df: DataFrame de entrada
        
    Returns:
        DataFrame com novas features
    """
    df = df.copy()
    if 'valor' in df.columns:
        df['valor_log'] = np.log1p(df['valor'])
        print(f"  ✅ Feature criada: valor_log")
    return df
