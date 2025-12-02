"""
Demonstração: Pipeline completo com validação Pandera
Mostra como integrar validação no pipeline de dados
"""

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check


# ============================================
# SCHEMAS
# ============================================

schema_entrada = DataFrameSchema({
    "id": Column(int, nullable=False),
    "valor": Column(float, Check.greater_than(0)),
    "hora": Column(int, Check.in_range(0, 23)),
    "categoria": Column(str, Check.isin(['A', 'B', 'C', 'D'])),
})


# ============================================
# FUNÇÕES DO PIPELINE
# ============================================

def extrair_dados(caminho):
    """Extrai dados de CSV"""
    print(f"  Lendo {caminho}...")
    try:
        df = pd.read_csv(caminho)
        print(f"  ✅ {len(df)} linhas carregadas")
        return df
    except FileNotFoundError:
        print(f"  ❌ Arquivo não encontrado: {caminho}")
        return None


def validar_dados(df):
    """Valida dados com Pandera"""
    print("  Validando schema...")
    try:
        schema_entrada.validate(df)
        print("  ✅ Schema válido!")
        return True
    except pa.errors.SchemaError as e:
        print("  ❌ Schema inválido!")
        print(f"     {e.failure_cases}")
        return False


def transformar_dados(df):
    """Transforma dados"""
    print("  Aplicando transformações...")
    df = df.copy()
    df = df.dropna()
    df = df.drop_duplicates()
    print(f"  ✅ {len(df)} linhas após limpeza")
    return df


def salvar_dados(df, caminho):
    """Salva dados processados"""
    print(f"  Salvando em {caminho}...")
    df.to_csv(caminho, index=False)
    print("  ✅ Dados salvos!")


# ============================================
# PIPELINE PRINCIPAL
# ============================================

def executar_pipeline(arquivo_entrada, arquivo_saida):
    """Executa pipeline completo com validação"""
    print("\n" + "="*50)
    print("PIPELINE COM VALIDAÇÃO")
    print("="*50)
    
    # Etapa 1: Extrair
    print("\n1/4 Extraindo...")
    df = extrair_dados(arquivo_entrada)
    if df is None:
        print("\n❌ Pipeline interrompido: erro na extração")
        return False
    
    # Etapa 2: Validar
    print("\n2/4 Validando...")
    if not validar_dados(df):
        print("\n❌ Pipeline interrompido: dados inválidos")
        return False
    
    # Etapa 3: Transformar
    print("\n3/4 Transformando...")
    df = transformar_dados(df)
    
    # Etapa 4: Salvar
    print("\n4/4 Salvando...")
    salvar_dados(df, arquivo_saida)
    
    print("\n" + "="*50)
    print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*50)
    return True


# ============================================
# DEMONSTRAÇÃO
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DEMONSTRAÇÃO: PIPELINE COM VALIDAÇÃO PANDERA")
    print("="*60)
    
    # Teste 1: Dados válidos
    print("\n\n>>> TESTE 1: Dados válidos")
    executar_pipeline('data/transacoes_ok.csv', 'data/output_ok.csv')
    
    # Teste 2: Dados com problemas
    print("\n\n>>> TESTE 2: Dados com problemas")
    executar_pipeline('data/transacoes_problema.csv', 'data/output_problema.csv')
