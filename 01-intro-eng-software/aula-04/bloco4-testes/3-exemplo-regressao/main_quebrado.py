"""
API de Detecção de Fraude - VERSÃO QUEBRADA (REGRESSÃO!)
Um gerente pediu para aumentar o threshold de R$ 10k para R$ 15k
Isso VIOLA a especificação original e quebra os testes!
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API Fraude - Versão Quebrada")


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
    return {"status": "API rodando", "versao": "1.1-quebrado"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analisar", response_model=ResultadoAnalise)
def analisar_transacao(transacao: Transacao):
    """
    Analisa uma transação e retorna se é fraude.
    
    ❌ REGRESSÃO: Gerente pediu para aumentar threshold para R$ 15.000
    Isso viola a regra de negócio original!
    """
    valor_processado = float(transacao.valor)
    
    # ❌ REGRESSÃO: threshold mudou de R$ 10.000 para R$ 15.000
    # Isso quebra a especificação e os testes vão falhar!
    if valor_processado > 15000:  # Era 10000 antes!
        return ResultadoAnalise(
            fraude=True,
            confianca=0.95,
            motivo="Valor acima do threshold de R$ 15.000"
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
