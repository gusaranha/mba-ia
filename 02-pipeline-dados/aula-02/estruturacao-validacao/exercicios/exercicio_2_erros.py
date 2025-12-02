"""
Exercício 2: Adicionar tratamento de erros

Funções básicas fornecidas. Sua tarefa:
- Adicionar try/except
- Tratar casos de erro
"""

import pandas as pd


# ============================================
# FUNÇÕES SEM TRATAMENTO (modificar)
# ============================================

def carregar_dados(caminho):
    """
    Carrega dados de CSV
    
    TODO: Adicionar tratamento para:
    - Arquivo não encontrado
    - Retornar None se houver erro
    """
    df = pd.read_csv(caminho)
    return df


def validar_colunas(df, colunas_esperadas):
    """
    Verifica se colunas existem
    
    TODO: Adicionar verificação de:
    - DataFrame None
    - Colunas faltando
    - Retornar True se válido, False se inválido
    """
    # Implementar aqui
    pass


def processar_dados(df):
    """
    Processa dados
    
    TODO: Adicionar verificação de:
    - DataFrame vazio
    - DataFrame None
    - Retornar None se inválido
    """
    df = df.dropna()
    return df


# ============================================
# PIPELINE COM TRATAMENTO
# ============================================

def executar_pipeline_seguro(caminho):
    """
    TODO: Implementar pipeline que:
    - Carrega dados
    - Valida colunas ['id', 'preco', 'quantidade', 'produto']
    - Processa dados
    - Imprime resultado ou erro apropriado
    """
    pass


# ============================================
# TESTE
# ============================================

if __name__ == "__main__":
    # Teste com arquivo existente
    # executar_pipeline_seguro('data/vendas.csv')
    
    # Teste com arquivo inexistente
    # executar_pipeline_seguro('data/nao_existe.csv')
    pass
