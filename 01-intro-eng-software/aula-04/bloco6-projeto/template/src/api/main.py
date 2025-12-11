from fastapi import FastAPI, HTTPException
from src.models.schemas import CalculoRequest, CalculoResponse
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Minha API - Template")

@app.get("/")
def health_check():
    """Endpoint de health check"""
    return {"status": "ok", "message": "API funcionando"}

@app.post("/calcular", response_model=CalculoResponse)
def calcular(dados: CalculoRequest):
    """
    Endpoint principal - SUBSTITUA esta lógica pela sua!
    
    Exemplo atual: soma simples de dois números
    """
    try:
        # 🎯 COLOQUE SUA LÓGICA AQUI
        resultado = dados.valor1 + dados.valor2
        
        logger.info(f"Cálculo realizado: {dados.valor1} + {dados.valor2} = {resultado}")
        
        return CalculoResponse(resultado=resultado)
        
    except Exception as e:
        logger.error(f"Erro ao calcular: {e}")
        raise HTTPException(status_code=500, detail=str(e))
