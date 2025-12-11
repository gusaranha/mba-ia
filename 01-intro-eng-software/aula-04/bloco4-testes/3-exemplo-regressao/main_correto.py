"""
API de Detecção de Fraude - VERSÃO CORRETA
Regra de negócio: Transações > R$ 10.000 são fraude
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API Fraude - Versão Correta")


class Transacao(BaseModel):
    valor: float
    hora_do_dia: int
    distancia_ultima_compra_km: float
    numero_transacoes_hoje: int
    idade_conta_dias: int


class ResultadoAnalise(BaseModel):
    fraude: bool
    confianca: float
    motivo: str


@app.get("/")
def root():
    return {"status": "API rodando", "versao": "1.0-correto"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analisar", response_model=ResultadoAnalise)
def analisar_transacao(transacao: Transacao):
    """
    Analisa uma transação e retorna se é fraude.
    
    Regra de negócio CORRETA: Transações > R$ 10.000 são consideradas fraude
    """
    valor_processado = float(transacao.valor)
    
    # ✅ REGRA CORRETA: threshold em R$ 10.000
    if valor_processado > 10000:
        return ResultadoAnalise(
            fraude=True,
            confianca=0.95,
            motivo="Valor acima do threshold de R$ 10.000"
        )
    
    if transacao.hora_do_dia < 6 or transacao.hora_do_dia > 23:
        return ResultadoAnalise(
            fraude=True,
            confianca=0.85,
            motivo="Transação em horário suspeito"
        )
    
    if transacao.distancia_ultima_compra_km > 500:
        return ResultadoAnalise(
            fraude=True,
            confianca=0.80,
            motivo="Distância muito grande da última compra"
        )
    
    return ResultadoAnalise(
        fraude=False,
        confianca=0.90,
        motivo="Transação dentro dos padrões normais"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
