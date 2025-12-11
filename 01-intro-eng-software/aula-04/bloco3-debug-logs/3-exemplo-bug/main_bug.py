"""
API de Detecção de Fraude - Versão COM BUG LÓGICO
Este exemplo demonstra um bug comum: perda de precisão com valores decimais.

🐛 BUG: Valores com centavos são arredondados para baixo, perdendo dados.
Exemplo: R$ 10,50 é processado como R$ 10,00
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Detecção de Fraude - Com Bug",
    description="Versão com bug lógico (perda de centavos)",
    version="1.0.0-buggy"
)


class TransacaoInput(BaseModel):
    valor: float = Field(..., gt=0, description="Valor da transação em reais")
    hora_do_dia: int = Field(..., ge=0, le=23, description="Hora da transação (0-23)")
    distancia_ultima_compra_km: float = Field(..., ge=0, description="Distância da última compra em km")
    numero_transacoes_hoje: int = Field(..., ge=0, description="Número de transações hoje")
    idade_conta_dias: int = Field(..., ge=0, description="Idade da conta em dias")


class TransacaoOutput(BaseModel):
    fraude: bool
    score_risco: float
    valor_processado: float
    mensagem: str
    debug_info: dict = None  # Para mostrar o bug


@app.get("/")
def root():
    return {
        "status": "API Detecção de Fraude - Com Bug",
        "version": "1.0.0-buggy",
        "warning": "Esta versão contém um bug lógico!"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analisar", response_model=TransacaoOutput)
def analisar_transacao(transacao: TransacaoInput):
    """
    Analisa uma transação e retorna se é provável fraude.
    
    🐛 BUG: Conversão incorreta de float para int perde os centavos!
    """
    
    try:
        # 🐛 BUG CRÍTICO: int() trunca valores decimais!
        # Exemplo: int(10.50) = 10 (perdeu R$ 0,50!)
        valor_processado = int(transacao.valor)
        
        # Lógica de detecção de fraude
        score_risco = 0.0
        
        # Regra 1: Valor alto
        if valor_processado > 10000:
            score_risco += 0.4
        
        # Regra 2: Horário suspeito
        if transacao.hora_do_dia < 6 or transacao.hora_do_dia > 23:
            score_risco += 0.3
        
        # Regra 3: Distância grande
        if transacao.distancia_ultima_compra_km > 500:
            score_risco += 0.2
        
        # Regra 4: Muitas transações
        if transacao.numero_transacoes_hoje > 10:
            score_risco += 0.1
        
        # Decisão
        fraude = score_risco >= 0.5
        
        if fraude:
            mensagem = "Transação bloqueada por suspeita de fraude"
        else:
            mensagem = "Transação aprovada"
        
        return TransacaoOutput(
            fraude=fraude,
            score_risco=round(score_risco, 2),
            valor_processado=valor_processado,
            mensagem=mensagem,
            debug_info={
                "valor_original": transacao.valor,
                "valor_processado": valor_processado,
                "diferenca_perdida": transacao.valor - valor_processado,
                "bug": "int() trunca valores decimais!"
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


if __name__ == "__main__":
    import uvicorn
    print("⚠️  Iniciando servidor COM BUG...")
    print("🐛 Teste com valor: 10.50 e veja o problema!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
