# bloco3-ml-fundamentos/api_ml.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import numpy as np

app = FastAPI(title="Detecção de Fraude - Machine Learning")

class Transacao(BaseModel):
    valor: float = Field(..., gt=0, description="Valor da transação em reais")
    hora: int = Field(..., ge=0, le=23, description="Hora da transação (0-23)")
    distancia_km: float = Field(..., ge=0, description="Distância da última compra em km")
    transacoes_hoje: int = Field(..., ge=1, description="Número de transações hoje")
    idade_conta_dias: int = Field(..., ge=0, description="Idade da conta em dias")

# Carregar modelo treinado
print("🤖 Carregando modelo ML...")
try:
    with open("modelo_fraude.pkl", "rb") as f:
        modelo = pickle.load(f)
    print("✓ Modelo carregado com sucesso!")
except FileNotFoundError:
    print("❌ Modelo não encontrado!")
    print("Execute primeiro: python gerar_modelo.py")
    modelo = None

def detectar_fraude_ml(transacao: Transacao) -> dict:
    """
    Detecção de fraude usando MACHINE LEARNING
    
    Vantagens desta abordagem:
    - Aprende padrões automaticamente dos dados
    - Considera combinações complexas de features
    - Pode ser retreinado com novos dados
    - Melhor acurácia (menos erros)
    """
    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo não disponível. Execute: python gerar_modelo.py"
        )
    
    # Preparar features na ORDEM CORRETA (mesmo ordem do treino)
    # [valor, hora, distancia_km, transacoes_hoje, idade_conta_dias]
    features = np.array([[
        transacao.valor,
        transacao.hora,
        transacao.distancia_km,
        transacao.transacoes_hoje,
        transacao.idade_conta_dias
    ]])
    
    # Fazer predição
    predicao = modelo.predict(features)[0]  # 0 = legítima, 1 = fraude
    probabilidades = modelo.predict_proba(features)[0]  # [prob_legitima, prob_fraude]
    
    # Pegar confiança da classe predita
    confianca = probabilidades[predicao]
    
    return {
        "fraude": bool(predicao == 1),
        "confianca": float(confianca),
        "metodo": "machine_learning",
        "probabilidade_legitima": float(probabilidades[0]),
        "probabilidade_fraude": float(probabilidades[1])
    }

@app.get("/")
def raiz():
    return {
        "api": "Detecção de Fraude - Machine Learning",
        "metodo": "Random Forest (aprendizado automático)",
        "vantagem": "Aprende padrões dos dados, melhor acurácia",
        "modelo_carregado": modelo is not None
    }

@app.get("/health")
def health():
    """Verifica se modelo está carregado"""
    return {
        "status": "healthy" if modelo is not None else "degraded",
        "modelo_carregado": modelo is not None
    }

@app.post("/analisar")
def analisar(transacao: Transacao):
    """
    Analisa transação usando MACHINE LEARNING
    
    Vantagens:
    - Aprende padrões complexos automaticamente
    - Considera todas as features em conjunto
    - Pode ser retreinado com novos dados
    - Melhor precisão que regras fixas
    """
    resultado = detectar_fraude_ml(transacao)
    
    # Definir nível de risco baseado na confiança
    if resultado["confianca"] >= 0.9:
        nivel_risco = "ALTO"
    elif resultado["confianca"] >= 0.7:
        nivel_risco = "MÉDIO"
    else:
        nivel_risco = "BAIXO"
    
    return {
        "transacao": transacao.dict(),
        "resultado": resultado,
        "nivel_risco": nivel_risco,
        "observacao": "✅ Este método aprende padrões automaticamente dos dados"
    }

# EXECUTAR:
# 1. Primeiro gere o modelo: python gerar_modelo.py
# 2. Depois rode a API: uvicorn api_ml:app --reload --port 8002
# Docs: http://localhost:8002/docs