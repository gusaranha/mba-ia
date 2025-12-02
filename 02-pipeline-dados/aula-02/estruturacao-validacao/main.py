"""
Pipeline principal - orquestra todas as etapas
"""

from pipeline.extract import extrair_dados
from pipeline.transform import limpar_dados, criar_features
from pipeline.load import salvar_dados


def executar_pipeline():
    """Executa pipeline completo"""
    print("="*50)
    print("EXECUTANDO PIPELINE")
    print("="*50)
    
    print("\n1/4 Extraindo dados...")
    df = extrair_dados('data/transacoes.csv')
    if df is None:
        print("\n❌ Pipeline interrompido!")
        return
    
    print("\n2/4 Limpando dados...")
    df = limpar_dados(df)
    
    print("\n3/4 Criando features...")
    df = criar_features(df)
    
    print("\n4/4 Salvando dados...")
    salvar_dados(df, 'data/processed.csv')
    
    print("\n" + "="*50)
    print("✅ PIPELINE CONCLUÍDO!")
    print("="*50)


if __name__ == "__main__":
    executar_pipeline()
