from fastapi import FastAPI
from src.models.schemas import ValidadorRequest, ValidadorResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Validador de CPF")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/validar", response_model=ValidadorResponse)
def validar_cpf(dados: ValidadorRequest):
    """
    Valida CPF de forma simplificada
    Regra: deve ter 11 dígitos numéricos
    """
    cpf_limpo = dados.cpf.replace(".", "").replace("-", "")
    
    valido = len(cpf_limpo) == 11 and cpf_limpo.isdigit()
    
    logger.info(f"CPF {dados.cpf} validado: {valido}")
    
    return ValidadorResponse(cpf=dados.cpf, valido=valido)
