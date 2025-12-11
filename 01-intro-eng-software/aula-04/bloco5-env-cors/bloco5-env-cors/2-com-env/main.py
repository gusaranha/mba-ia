"""
API Simples de Detecção de Fraude - COM Variáveis de Ambiente
✅ SOLUÇÃO: Configurações externas via .env
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import os
from dotenv import load_dotenv

# ✅ SOLUÇÃO: Carregar variáveis do arquivo .env
load_dotenv()

# ✅ SOLUÇÃO: Ler configurações de variáveis de ambiente
APP_NAME = os.getenv("APP_NAME", "Fraud Detection API")
VERSION = os.getenv("VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/models/fraud_detection_model.pkl")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
FRAUD_THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", "10000"))

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
    environment: str
    timestamp: str


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": f"Bem-vindo à {APP_NAME}",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "app_name": APP_NAME,
        "version": VERSION,
        "environment": ENVIRONMENT
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_fraud(transaction: Transaction):
    """
    Prediz se uma transação é fraudulenta
    
    ✅ SOLUÇÃO: Threshold vem de variável de ambiente
    Para mudar, basta editar o .env e reiniciar!
    """
    
    # Lógica simples baseada em regras
    is_fraud = transaction.valor > FRAUD_THRESHOLD
    
    # Simular probabilidade
    probability = min(transaction.valor / FRAUD_THRESHOLD, 1.0) if is_fraud else 0.0
    
    return PredictionResponse(
        prediction=1 if is_fraud else 0,
        probability=round(probability, 4),
        label="FRAUDE" if is_fraud else "LEGÍTIMA",
        valor_analisado=transaction.valor,
        threshold=FRAUD_THRESHOLD,
        environment=ENVIRONMENT,
        timestamp=datetime.now().isoformat()
    )


@app.get("/config")
async def get_config():
    """
    Mostra configurações atuais
    
    ✅ SOLUÇÃO: Mostra configs de variáveis de ambiente
    (Obviamente, NUNCA mostre senhas aqui!)
    """
    return {
        "app_name": APP_NAME,
        "version": VERSION,
        "environment": ENVIRONMENT,
        "model_path": MODEL_PATH,
        "log_level": LOG_LEVEL,
        "fraud_threshold": FRAUD_THRESHOLD,
        "message": "✅ Todas essas configs vêm do arquivo .env!"
    }


if __name__ == "__main__":
    import uvicorn
    
    # ✅ SOLUÇÃO: Host e porta também vêm de variáveis de ambiente
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "8000"))
    
    print(f"✅ Configurações carregadas do .env:")
    print(f"   - APP_NAME: {APP_NAME}")
    print(f"   - ENVIRONMENT: {ENVIRONMENT}")
    print(f"   - MODEL_PATH: {MODEL_PATH}")
    print(f"   - LOG_LEVEL: {LOG_LEVEL}")
    print(f"   - FRAUD_THRESHOLD: {FRAUD_THRESHOLD}")
    print(f"   - HOST: {HOST}")
    print(f"   - PORT: {PORT}")
    print(f"\n✅ Para mudar qualquer config, edite o .env e reinicie!\n")
    
    uvicorn.run(app, host=HOST, port=PORT)
