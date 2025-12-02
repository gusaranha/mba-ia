"""
Módulo de salvamento de dados
"""

import pandas as pd


def salvar_dados(df, caminho):
    """
    Salva DataFrame em arquivo CSV.
    
    Args:
        df: DataFrame a ser salvo
        caminho: Caminho do arquivo de saída
    """
    try:
        df.to_csv(caminho, index=False)
        print(f"  ✅ Dados salvos em {caminho}")
    except Exception as e:
        print(f"  ❌ Erro ao salvar: {e}")
