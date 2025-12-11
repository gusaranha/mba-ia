"""
Aplicação principal da API de Machine Learning
"""
import logging
from fastapi import FastAPI, HTTPException, Depends
from src.data.schemas import CalculatorInput, CalculatorOutput
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from  src.models.model_loader import ModelLoader
from pathlib import Path
from src.api.dependencies import get_model_loader
from src.data.schemas import TransactionInput, FraudPredictionOutput

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando a API")
    model_loader = ModelLoader()
    model_loader.load_model(Path("artifacts/models/fraud_detection_model.pkl"))
    yield
    logger.info("Finalizando a API")

app = FastAPI(
    lifespan=lifespan,
    title="Aula 02",
    version="1.0",
    description="API de Machine Learning",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return {"message": "Welcome to the ML Model API!"}

@app.post("/calcular", response_model=CalculatorOutput)
def calcular(entrada:CalculatorInput):
    """Realiza operações matemáticas básicas"""
    logger.info("Calculando %s %s %s", entrada.numero1, entrada.operacao, entrada.numero2)

    num1 = entrada.numero1
    num2 = entrada.numero2
    operacao = entrada.operacao

    if operacao == "+":
        resultado = num1 + num2
    elif operacao == "-":
        resultado = num1 - num2
    elif operacao == "*":
        resultado = num1 * num2
    elif operacao == "/":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Divisão por zero não é permitida.")
        resultado = num1 / num2
    else:
        raise HTTPException(status_code=400, detail="Operação inválida.")

    return CalculatorOutput(
        resultado=resultado,
        operacao=operacao,
        expressao=f"{num1} {operacao} {num2} = {resultado}"
    )


# Função auxiliar para determinar nível de risco
def get_risk_level(probability: float) -> str:
    """Determina nível de risco baseado na probabilidade"""
    if probability < 0.3:
        return "BAIXO"
    elif probability < 0.7:
        return "MÉDIO"
    else:
        return "ALTO"


@app.post("/predict", response_model=FraudPredictionOutput)
def predict_fraud(
        transaction: TransactionInput,
        model_loader: ModelLoader = Depends(get_model_loader)):
    """Deteta Fraude"""
    logger.info(f"Analise de transaçao : Amount={transaction.Amount}")

    try:
        # Extrair features como lista (ordem importa!)
        features = [
            transaction.Time,
            transaction.V1, transaction.V2, transaction.V3, transaction.V4, transaction.V5,
            transaction.V6, transaction.V7, transaction.V8, transaction.V9, transaction.V10,
            transaction.Amount
        ]

        # Fazer predição
        prediction, fraud_probability = model_loader.predict(features)

        # Determinar label e risk level
        prediction_label = "FRAUDULENTA" if prediction == 1 else "LEGÍTIMA"
        risk_level = get_risk_level(fraud_probability)

        logger.info(f"✅ Resultado: {prediction_label} (prob: {fraud_probability:.4f}, risco: {risk_level})")

        return FraudPredictionOutput(
            prediction=prediction,
            prediction_label=prediction_label,
            fraud_probability=fraud_probability,
            risk_level=risk_level,
            model_version="1.0.0"
        )

    except Exception as e:
        logger.error(f"❌ Erro na predição: {e}", exc_info=True)
        raise
