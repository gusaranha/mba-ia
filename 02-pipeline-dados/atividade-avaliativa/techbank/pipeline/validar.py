"""
Pipeline - Etapa 2: Validar Dados com Pandera
"""

import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema


def criar_schema():
    """
    Cria o schema de validação para o dataset de clientes.
    
    Returns:
        DataFrameSchema do Pandera
    """
    
    schema = DataFrameSchema({
        
        # TODO 1: Validar cliente_id
        # - Tipo: int
        # - Não pode ser nulo (nullable=False)
        # - Deve ser único (unique=True)
        # Dica: "cliente_id": Column(int, nullable=False, unique=True),
        
        "cliente_id": None,  # Substitua None pelo código correto
        
        
        # TODO 2: Validar idade
        # - Tipo: int
        # - Valores entre 18 e 80
        # Dica: Column(int, Check.in_range(18, 80)),
        
        "idade": None,  # Substitua None pelo código correto
        
        
        # TODO 3: Validar renda_mensal
        # - Tipo: float
        # - Valores entre 1000 e 50000
        
        "renda_mensal": None,  # Substitua None pelo código correto
        
        
        # Estas validações já estão prontas como exemplo:
        "tempo_conta_meses": Column(int, Check.in_range(1, 240)),
        "num_produtos": Column(int, Check.in_range(1, 5)),
        "tem_cartao_credito": Column(int, Check.isin([0, 1])),
        
        
        # TODO 4: Validar score_credito
        # - Tipo: float
        # - Valores entre 300 e 850
        
        "score_credito": None,  # Substitua None pelo código correto
        
        
        # TODO 5: Validar respondeu_campanha (target)
        # - Tipo: int
        # - Valores permitidos: 0 ou 1
        # Dica: Column(int, Check.isin([0, 1])),
        
        "respondeu_campanha": None,  # Substitua None pelo código correto
        
    })
    
    return schema


def validar_dados(df):
    """
    Valida o DataFrame usando o schema definido.
    
    Args:
        df: DataFrame a ser validado
        
    Returns:
        DataFrame validado (ou levanta exceção se inválido)
    """
    schema = criar_schema()
    
    print("Validando dados...")
    
    try:
        df_validado = schema.validate(df)
        print("✅ Dados válidos!")
        return df_validado
    except pa.errors.SchemaError as e:
        print("❌ Dados inválidos!")
        print(f"Erro: {e}")
        raise


# Teste local
if __name__ == "__main__":
    # Carregar dados para teste
    df = pd.read_csv("data/clientes_campanha.csv")
    
    # Tentar validar
    try:
        df_validado = validar_dados(df)
        print(f"\n{len(df_validado)} registros validados com sucesso!")
    except Exception as e:
        print(f"\nFalha na validação. Verifique os TODOs!")
