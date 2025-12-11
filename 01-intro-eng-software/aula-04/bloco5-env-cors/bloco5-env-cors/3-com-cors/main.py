"""
API Simples de Detecção de Fraude - COM CORS
✅ SOLUÇÃO: Frontend pode consumir a API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações
APP_NAME = os.getenv("APP_NAME", "Fraud Detection API")
VERSION = os.getenv("VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/models/fraud_detection_model.pkl")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
FRAUD_THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", "10000"))

# ✅ CORS: Ler origens permitidas do .env
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)

# ========================================
# ✅ CONFIGURAR CORS
# ========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Origens permitidas
    allow_credentials=True,       # Permite cookies/auth
    allow_methods=["*"],          # Permite GET, POST, PUT, DELETE, etc
    allow_headers=["*"],          # Permite qualquer header
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
    cors_enabled: bool
    timestamp: str


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": f"Bem-vindo à {APP_NAME}",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "cors_enabled": True,
        "cors_origins": CORS_ORIGINS,
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
        "environment": ENVIRONMENT,
        "cors_enabled": True
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_fraud(transaction: Transaction):
    """
    Prediz se uma transação é fraudulenta
    
    ✅ Agora pode ser chamado de qualquer frontend!
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
        cors_enabled=True,
        timestamp=datetime.now().isoformat()
    )


@app.get("/config")
async def get_config():
    """Mostra configurações atuais"""
    return {
        "app_name": APP_NAME,
        "version": VERSION,
        "environment": ENVIRONMENT,
        "model_path": MODEL_PATH,
        "log_level": LOG_LEVEL,
        "fraud_threshold": FRAUD_THRESHOLD,
        "cors_enabled": True,
        "cors_origins": CORS_ORIGINS,
        "message": "✅ Configurações do .env + CORS habilitado!"
    }


if __name__ == "__main__":
    import uvicorn
    
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "8000"))
    
    print(f"✅ Configurações carregadas:")
    print(f"   - APP_NAME: {APP_NAME}")
    print(f"   - ENVIRONMENT: {ENVIRONMENT}")
    print(f"   - FRAUD_THRESHOLD: {FRAUD_THRESHOLD}")
    print(f"   - HOST: {HOST}")
    print(f"   - PORT: {PORT}")
    print(f"\n✅ CORS habilitado!")
    print(f"   - Origens permitidas: {CORS_ORIGINS}")
    print(f"\n🌐 Frontend pode consumir esta API!\n")
    
    uvicorn.run(app, host=HOST, port=PORT)
