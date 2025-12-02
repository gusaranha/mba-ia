"""
Pipeline Principal - Classificação de Resposta a Campanha
=========================================================

Execute este arquivo após completar todos os TODOs:
    python main.py

O pipeline executa 4 etapas:
    1. Carregar e explorar dados
    2. Validar dados com Pandera
    3. Treinar modelo
    4. Avaliar e exibir resultados
"""

from pipeline.carregar import carregar_dados, explorar_dados, verificar_target
from pipeline.validar import validar_dados
from pipeline.treinar import preparar_dados, dividir_treino_teste, treinar_modelo, salvar_modelo
from pipeline.avaliar import avaliar_modelo, exibir_resultados


def executar_pipeline():
    """
    Executa o pipeline completo de ML.
    """
    
    print("\n" + "🚀" * 20)
    print("INICIANDO PIPELINE DE ML")
    print("🚀" * 20 + "\n")
    
    # =========================================
    # ETAPA 1: CARREGAR E EXPLORAR
    # =========================================
    print("\n[ETAPA 1/4] Carregando dados...")
    
    df = carregar_dados("data/clientes_campanha.csv")
    
    if df is None:
        print("❌ ERRO: Dados não carregados. Complete TODO 1 em carregar.py")
        return
    
    explorar_dados(df)
    verificar_target(df)
    
    # =========================================
    # ETAPA 2: VALIDAR
    # =========================================
    print("\n[ETAPA 2/4] Validando dados...")
    
    try:
        df_validado = validar_dados(df)
    except Exception as e:
        print(f"❌ ERRO na validação. Complete os TODOs em validar.py")
        print(f"Detalhes: {e}")
        return
    
    # =========================================
    # ETAPA 3: TREINAR
    # =========================================
    print("\n[ETAPA 3/4] Treinando modelo...")
    
    X, y = preparar_dados(df_validado)
    
    if X is None or y is None:
        print("❌ ERRO: Dados não preparados. Complete TODOs 1-2 em treinar.py")
        return
    
    X_train, X_test, y_train, y_test = dividir_treino_teste(X, y)
    
    if X_train is None:
        print("❌ ERRO: Split não realizado. Complete TODO 3 em treinar.py")
        return
    
    modelo = treinar_modelo(X_train, y_train)
    
    if modelo is None:
        print("❌ ERRO: Modelo não treinado. Complete TODOs 4-5 em treinar.py")
        return
    
    salvar_modelo(modelo)
    
    # =========================================
    # ETAPA 4: AVALIAR
    # =========================================
    print("\n[ETAPA 4/4] Avaliando modelo...")
    
    metricas, y_pred = avaliar_modelo(modelo, X_test, y_test)
    f1_final = exibir_resultados(metricas, y_test, y_pred)
    
    # =========================================
    # FINALIZAÇÃO
    # =========================================
    print("\n" + "✅" * 20)
    print("PIPELINE CONCLUÍDO COM SUCESSO!")
    print("✅" * 20)
    print(f"\n📝 Anote o F1-Score no arquivo RESPOSTAS.md: {f1_final:.4f}")
    print("\n")


if __name__ == "__main__":
    executar_pipeline()
