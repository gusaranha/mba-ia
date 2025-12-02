"""
Exercício 3: GABARITO
Criar schema Pandera
"""

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check


# ============================================
# DADOS DE TESTE
# ============================================

df_valido = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, 150.00, 89.90],
    'quantidade': [2, 1, 5],
    'produto': ['Livro', 'Eletro', 'Roupa']
})

df_preco_negativo = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, -150.00, 89.90],
    'quantidade': [2, 1, 5],
    'produto': ['Livro', 'Eletro', 'Roupa']
})

df_qtd_zero = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, 150.00, 89.90],
    'quantidade': [0, 1, 5],
    'produto': ['Livro', 'Eletro', 'Roupa']
})

df_produto_invalido = pd.DataFrame({
    'id': [1, 2, 3],
    'preco': [29.90, 150.00, 89.90],
    'quantidade': [2, 1, 5],
    'produto': ['Livro', 'Celular', 'Roupa']
})


# ============================================
# SCHEMA
# ============================================

schema_vendas = DataFrameSchema({
    "id": Column(int, nullable=False),
    "preco": Column(float, Check.greater_than(0)),
    "quantidade": Column(int, Check.greater_than_or_equal_to(1)),
    "produto": Column(str, Check.isin(['Livro', 'Eletro', 'Roupa'])),
})


# ============================================
# FUNÇÃO DE TESTE
# ============================================

def testar_schema(nome, df):
    """Testa um dataset com o schema"""
    print(f"\n--- Testando: {nome} ---")
    
    try:
        schema_vendas.validate(df)
        print("✅ Dados válidos!")
    except pa.errors.SchemaError as e:
        print("❌ Dados inválidos!")
        print(f"   Detalhes: {e.failure_cases}")


# ============================================
# TESTE
# ============================================

if __name__ == "__main__":
    print("="*50)
    print("TESTANDO SCHEMA DE VENDAS")
    print("="*50)
    
    testar_schema("Válido", df_valido)
    testar_schema("Preço negativo", df_preco_negativo)
    testar_schema("Quantidade zero", df_qtd_zero)
    testar_schema("Produto inválido", df_produto_invalido)
