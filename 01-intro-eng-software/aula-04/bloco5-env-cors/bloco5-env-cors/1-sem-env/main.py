"""
API Simples de Detecção de Fraude - SEM Variáveis de Ambiente
❌ PROBLEMA: Tudo hardcoded no código
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

# ❌ PROBLEMA: Configurações hardcoded
APP_NAME = "Fraud Detection API"
VERSION = "1.0.0"
MODEL_PATH = "artifacts/models/fraud_detection_model.pkl"
LOG_LEVEL = "INFO"
FRAUD_THRESHOLD = 10000

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)


class Transaction(BaseModel):
    """Modelo de transação"""
    valor: float = Field(..., gt=0, description="Valor da transação em R$")
    hora_do_dia: int = Field(..., ge=0, le=23, description="Hora da transação (0-23)")
    distancia_ultima_compra_km: float = Field(..., ge=0, description="Distância da última compra em km")
    numero_transacoes_hoje: int = Field(..., ge=0, description="Número de transações hoje")
    idade_conta_dias: int = Field(..., ge=0, description="Idade da conta em dias")


class PredictionResponse(BaseModel):
    """Resposta da predição"""
    prediction: int
    probability: float
    label: str
    valor_analisado: float
    threshold: float
    timestamp: str


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": f"Bem-vindo à {APP_NAME}",
        "version": VERSION,
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "app_name": APP_NAME,
        "version": VERSION
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_fraud(transaction: Transaction):
    """
    Prediz se uma transação é fraudulenta
    
    ❌ PROBLEMA: Threshold hardcoded
    Se quiser mudar, tem que alterar o código!
    """
    
    # Lógica simples baseada em regras
    # (Em produção, usaria modelo ML)
    is_fraud = transaction.valor > FRAUD_THRESHOLD
    
    # Simular probabilidade
    probability = min(transaction.valor / FRAUD_THRESHOLD, 1.0) if is_fraud else 0.0
    
    return PredictionResponse(
        prediction=1 if is_fraud else 0,
        probability=round(probability, 4),
        label="FRAUDE" if is_fraud else "LEGÍTIMA",
        valor_analisado=transaction.valor,
        threshold=FRAUD_THRESHOLD,
        timestamp=datetime.now().isoformat()
    )


@app.get("/config")
async def get_config():
    """
    Mostra configurações atuais
    
    ❌ PROBLEMA: Expõe configurações hardcoded
    """
    return {
        "app_name": APP_NAME,
        "version": VERSION,
        "model_path": MODEL_PATH,
        "log_level": LOG_LEVEL,
        "fraud_threshold": FRAUD_THRESHOLD,
        "warning": "Todas essas configs estão HARDCODED no código!"
    }


if __name__ == "__main__":
    import uvicorn
    
    # ❌ PROBLEMA: Host e porta hardcoded
    print(f"⚠️  AVISO: Configurações hardcoded!")
    print(f"   - APP_NAME: {APP_NAME}")
    print(f"   - MODEL_PATH: {MODEL_PATH}")
    print(f"   - LOG_LEVEL: {LOG_LEVEL}")
    print(f"   - FRAUD_THRESHOLD: {FRAUD_THRESHOLD}")
    print(f"\n❌ Para mudar qualquer config, tem que ALTERAR O CÓDIGO!\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
