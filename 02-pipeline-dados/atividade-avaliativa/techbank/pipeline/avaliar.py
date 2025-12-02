"""
Pipeline - Etapa 4: Avaliar Modelo
(Este arquivo está PRONTO - não precisa modificar)
"""

from sklearn.metrics import (
    f1_score, 
    accuracy_score, 
    precision_score, 
    recall_score,
    confusion_matrix,
    classification_report
)


def avaliar_modelo(modelo, X_test, y_test):
    """
    Avalia o modelo usando várias métricas.
    
    Args:
        modelo: modelo treinado
        X_test: features de teste
        y_test: target de teste
        
    Returns:
        Dicionário com métricas
    """
    
    # Fazer predições
    y_pred = modelo.predict(X_test)
    
    # Calcular métricas
    metricas = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1_score': f1_score(y_test, y_pred, zero_division=0)
    }
    
    return metricas, y_pred


def exibir_resultados(metricas, y_test, y_pred):
    """
    Exibe os resultados de forma formatada.
    
    Args:
        metricas: dicionário com métricas
        y_test: valores reais
        y_pred: valores preditos
    """
    
    print("\n" + "=" * 50)
    print("RESULTADOS DA AVALIAÇÃO")
    print("=" * 50)
    
    print(f"\n📊 MÉTRICAS:")
    print(f"   Accuracy:  {metricas['accuracy']:.4f} ({metricas['accuracy']*100:.2f}%)")
    print(f"   Precision: {metricas['precision']:.4f}")
    print(f"   Recall:    {metricas['recall']:.4f}")
    print(f"   F1-Score:  {metricas['f1_score']:.4f}")
    
    print(f"\n📋 MATRIZ DE CONFUSÃO:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"   Verdadeiros Negativos (TN): {cm[0,0]}")
    print(f"   Falsos Positivos (FP):      {cm[0,1]}")
    print(f"   Falsos Negativos (FN):      {cm[1,0]}")
    print(f"   Verdadeiros Positivos (TP): {cm[1,1]}")
    
    print("\n" + "=" * 50)
    print(f"🎯 F1-SCORE FINAL: {metricas['f1_score']:.4f}")
    print("=" * 50)
    
    return metricas['f1_score']
