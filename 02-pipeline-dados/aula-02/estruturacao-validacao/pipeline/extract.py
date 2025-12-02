"""
Módulo de extração de dados
"""

import pandas as pd


def extrair_dados(caminho):
    """
    Lê dados de arquivo CSV.
    
    Args:
        caminho: Caminho para o arquivo CSV
        
    Returns:
        DataFrame com os dados ou None se houver erro
    """
    try:
        df = pd.read_csv(caminho)
        print(f"  ✅ {len(df)} linhas carregadas de {caminho}")
        return df
    except FileNotFoundError:
        print(f"  ❌ Arquivo não encontrado: {caminho}")
        return None
    except Exception as e:
        print(f"  ❌ Erro ao ler arquivo: {e}")
        return None
