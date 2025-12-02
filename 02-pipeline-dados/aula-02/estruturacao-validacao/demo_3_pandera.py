"""
Demonstração: Introdução ao Pandera
Mostra validação declarativa de dados com Pandera
"""

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check


# ============================================
# DEFINIR SCHEMA
# ============================================

schema = DataFrameSchema({
    "id": Column(int, nullable=False),
    "valor": Column(float, Check.greater_than(0)),
    "hora": Column(int, Check.in_range(0, 23)),
    "categoria": Column(str, Check.isin(['A', 'B', 'C', 'D'])),
})


# ============================================
# DADOS DE TESTE
# ============================================

# Dataset VÁLIDO
df_valido = pd.DataFrame({
    'id': [1, 2, 3],
    'valor': [100.0, 250.5, 1500.0],
    'hora': [10, 15, 20],
    'categoria': ['A', 'B', 'C']
})

# Dataset com VALOR NEGATIVO
df_valor_negativo = pd.DataFrame({
    'id': [1, 2, 3],
    'valor': [100.0, -250.5, 1500.0],
    'hora': [10, 15, 20],
    'categoria': ['A', 'B', 'C']
})

# Dataset com HORA INVÁLIDA
df_hora_invalida = pd.DataFrame({
    'id': [1, 2, 3],
    'valor': [100.0, 250.5, 1500.0],
    'hora': [10, 25, 20],
    'categoria': ['A', 'B', 'C']
})

# Dataset com CATEGORIA INVÁLIDA
df_categoria_invalida = pd.DataFrame({
    'id': [1, 2, 3],
    'valor': [100.0, 250.5, 1500.0],
    'hora': [10, 15, 20],
    'categoria': ['A', 'X', 'C']
})


# ============================================
# FUNÇÃO DE TESTE
# ============================================

def testar_dataset(nome, df):
    """Testa um dataset com o schema"""
    print(f"\n--- Testando: {nome} ---")
    print(df)
    print()
    
    try:
        schema.validate(df)
        print("✅ Dados válidos!")
    except pa.errors.SchemaError as e:
        print(f"❌ Dados inválidos!")
        print(f"   Erro: {e.failure_cases}")


# ============================================
# DEMONSTRAÇÃO
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DEMONSTRAÇÃO: PANDERA BÁSICO")
    print("="*60)
    
    testar_dataset("Dataset válido", df_valido)
    testar_dataset("Valor negativo", df_valor_negativo)
    testar_dataset("Hora inválida", df_hora_invalida)
    testar_dataset("Categoria inválida", df_categoria_invalida)
    
    print("\n" + "="*60)
    print("CONCLUSÃO")
    print("="*60)
    print("""
PANDERA detectou automaticamente:
  → Valor negativo (deveria ser > 0)
  → Hora fora do range (deveria ser 0-23)
  → Categoria inválida (deveria ser A, B, C ou D)

Benefícios:
  → Menos código que validação manual
  → Mensagens de erro automáticas
  → Schema documenta os dados esperados
    """)
