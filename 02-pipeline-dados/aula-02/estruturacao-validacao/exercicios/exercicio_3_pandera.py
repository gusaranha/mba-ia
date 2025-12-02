"""
Exercício 3: Criar schema Pandera

Dataset de vendas fornecido. Sua tarefa:
- Criar schema com validações
- Testar com dados válidos e inválidos
"""

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check


# ============================================
# DADOS DE TESTE
# ============================================

# Dataset VÁLIDO
df_valido = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, 150.00, 89.90],
    'quantidade': [2, 1, 5],
    'produto': ['Livro', 'Eletro', 'Roupa']
})

# Dataset com PREÇO NEGATIVO
df_preco_negativo = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, -150.00, 89.90],
    'quantidade': [2, 1, 5],
    'produto': ['Livro', 'Eletro', 'Roupa']
})

# Dataset com QUANTIDADE ZERO
df_qtd_zero = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, 150.00, 89.90],
    'quantidade': [0, 1, 5],
    'produto': ['Livro', 'Eletro', 'Roupa']
})

# Dataset com PRODUTO INVÁLIDO
df_produto_invalido = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, 150.00, 89.90],
    'quantidade': [2, 1, 5],
    'produto': ['Livro', 'Celular', 'Roupa']
})


# ============================================
# TODO: CRIAR SCHEMA
# ============================================

# TODO 1: Criar schema com as seguintes regras:
# - id: inteiro, não nulo
# - preco: float, maior que 0
# - quantidade: inteiro, maior ou igual a 1
# - produto: string, deve ser 'Livro', 'Eletro' ou 'Roupa'

schema_vendas = DataFrameSchema({
    # Preencher aqui
})


# ============================================
# TODO: FUNÇÃO DE TESTE
# ============================================

def testar_schema(nome, df):
    """
    TODO: Implementar função que:
    - Tenta validar df com schema_vendas
    - Imprime ✅ se válido
    - Imprime ❌ e detalhes se inválido
    """
    pass


# ============================================
# TESTE
# ============================================

if __name__ == "__main__":
    # Descomentar quando implementar:
    # testar_schema("Válido", df_valido)
    # testar_schema("Preço negativo", df_preco_negativo)
    # testar_schema("Quantidade zero", df_qtd_zero)
    # testar_schema("Produto inválido", df_produto_invalido)
    pass
