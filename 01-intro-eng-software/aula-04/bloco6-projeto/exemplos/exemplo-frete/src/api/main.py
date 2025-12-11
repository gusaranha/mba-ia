from fastapi import FastAPI
from src.models.schemas import FreteRequest, FreteResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Calculadora de Frete")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/calcular", response_model=FreteResponse)
def calcular_frete(dados: FreteRequest):
    """
    Calcula frete baseado em peso e distância
    Regra: R$ 10 por kg + R$ 0,50 por km
    """
    valor_frete = (dados.peso * 10) + (dados.distancia * 0.5)
    
    logger.info(f"Frete calculado: peso={dados.peso}kg, distancia={dados.distancia}km, valor={valor_frete}")
    
    return FreteResponse(valor_frete=round(valor_frete, 2))
