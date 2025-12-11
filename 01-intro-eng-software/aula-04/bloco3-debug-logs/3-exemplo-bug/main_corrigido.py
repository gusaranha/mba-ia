"""
API de Detecção de Fraude - Versão CORRIGIDA
Este exemplo demonstra a correção do bug de perda de precisão.

✅ CORREÇÃO: Valores com centavos são preservados corretamente.
Exemplo: R$ 10,50 é processado como R$ 10,50
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Detecção de Fraude - Corrigida",
    description="Versão com bug corrigido (mantém centavos)",
    version="1.0.1-fixed"
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
    debug_info: dict = None  # Para mostrar a correção


@app.get("/")
def root():
    return {
        "status": "API Detecção de Fraude - Corrigida",
        "version": "1.0.1-fixed",
        "fix": "Bug de centavos corrigido!"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analisar", response_model=TransacaoOutput)
def analisar_transacao(transacao: TransacaoInput):
    """
    Analisa uma transação e retorna se é provável fraude.
    
    ✅ CORREÇÃO: float() mantém os centavos corretamente!
    """
    
    try:
        # ✅ CORREÇÃO: float() mantém valores decimais
        # Exemplo: float(10.50) = 10.50 (manteve R$ 0,50!)
        valor_processado = float(transacao.valor)
        
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
            valor_processado=round(valor_processado, 2),
            mensagem=mensagem,
            debug_info={
                "valor_original": transacao.valor,
                "valor_processado": round(valor_processado, 2),
                "diferenca_perdida": 0.0,
                "fix": "float() mantém valores decimais!"
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


if __name__ == "__main__":
    import uvicorn
    print("✅ Iniciando servidor CORRIGIDO...")
    print("🎉 Teste com valor: 10.50 e veja a correção!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
