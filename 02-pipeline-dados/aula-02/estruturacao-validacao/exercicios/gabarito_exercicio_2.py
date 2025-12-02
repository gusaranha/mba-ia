"""
Exercício 2: GABARITO
Adicionar tratamento de erros
"""

import pandas as pd


def carregar_dados(caminho):
    """Carrega dados de CSV com tratamento de erro"""
    try:
        df = pd.read_csv(caminho)
        print(f"✅ Carregado: {len(df)} linhas")
        return df
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho}")
        return None


def validar_colunas(df, colunas_esperadas):
    """Verifica se colunas existem"""
    if df is None:
        print("❌ DataFrame é None")
        return False
    
    colunas_faltando = []
    for col in colunas_esperadas:
        if col not in df.columns:
            colunas_faltando.append(col)
    
    if colunas_faltando:
        print(f"❌ Colunas faltando: {colunas_faltando}")
        return False
    
    print("✅ Todas as colunas presentes")
    return True


def processar_dados(df):
    """Processa dados com verificações"""
    if df is None:
        print("❌ DataFrame é None")
        return None
    
    if len(df) == 0:
        print("❌ DataFrame está vazio")
        return None
    
    df = df.dropna()
    print(f"✅ Processado: {len(df)} linhas")
    return df


def executar_pipeline_seguro(caminho):
    """Pipeline completo com tratamento de erros"""
    print("="*40)
    print(f"Processando: {caminho}")
    print("="*40)
    
    # Carregar
    print("\n1. Carregando...")
    df = carregar_dados(caminho)
    if df is None:
        print("\n❌ Pipeline interrompido!")
        return
    
    # Validar
    print("\n2. Validando...")
    colunas = ['id', 'preco', 'quantidade', 'produto']
    if not validar_colunas(df, colunas):
        print("\n❌ Pipeline interrompido!")
        return
    
    # Processar
    print("\n3. Processando...")
    df = processar_dados(df)
    if df is None:
        print("\n❌ Pipeline interrompido!")
        return
    
    print("\n✅ Pipeline concluído com sucesso!")
    print(f"   Linhas processadas: {len(df)}")


if __name__ == "__main__":
    print("\n>>> Teste 1: Arquivo existe")
    executar_pipeline_seguro('data/vendas.csv')
    
    print("\n\n>>> Teste 2: Arquivo não existe")
    executar_pipeline_seguro('data/nao_existe.csv')
