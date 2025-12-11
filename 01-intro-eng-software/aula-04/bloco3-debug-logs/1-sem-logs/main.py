"""
API de Detecção de Fraude - Versão SEM LOGS ESTRUTURADOS
Este exemplo demonstra uma API que usa print() ao invés de logging adequado.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Detecção de Fraude - Sem Logs",
    description="Exemplo de API sem logging estruturado",
    version="1.0.0"
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


@app.get("/")
def root():
    return {"status": "API Detecção de Fraude - Sem Logs", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analisar", response_model=TransacaoOutput)
def analisar_transacao(transacao: TransacaoInput):
    """
    Analisa uma transação e retorna se é provável fraude.
    
    ❌ Problema: Esta versão usa print() ao invés de logging estruturado.
    """
    
    # ❌ Print genérico - sem contexto, sem estrutura
    print("Recebida transação")
    
    try:
        # Validação básica
        if transacao.valor <= 0:
            print("ERRO! Valor inválido")  # ❌ Print genérico
            raise HTTPException(status_code=400, detail="Valor deve ser positivo")
        
        # Processamento
        valor_processado = transacao.valor
        
        # Lógica de detecção de fraude
        score_risco = 0.0
        
        # Regra 1: Valor alto
        if transacao.valor > 10000:
            score_risco += 0.4
            print("Valor alto detectado")  # ❌ Sem contexto
        
        # Regra 2: Horário suspeito
        if transacao.hora_do_dia < 6 or transacao.hora_do_dia > 23:
            score_risco += 0.3
            print("Horário suspeito")  # ❌ Sem contexto
        
        # Regra 3: Distância grande
        if transacao.distancia_ultima_compra_km > 500:
            score_risco += 0.2
            print("Distância grande")  # ❌ Sem contexto
        
        # Regra 4: Muitas transações
        if transacao.numero_transacoes_hoje > 10:
            score_risco += 0.1
            print("Muitas transações")  # ❌ Sem contexto
        
        # Decisão
        fraude = score_risco >= 0.5
        
        if fraude:
            print("FRAUDE DETECTADA!")  # ❌ Print inútil em produção
            mensagem = "Transação bloqueada por suspeita de fraude"
        else:
            print("Transação aprovada")  # ❌ Print inútil em produção
            mensagem = "Transação aprovada"
        
        return TransacaoOutput(
            fraude=fraude,
            score_risco=round(score_risco, 2),
            valor_processado=valor_processado,
            mensagem=mensagem
        )
    
    except ValueError as e:
        print(f"ERRO: {e}")  # ❌ Sem estrutura, sem contexto
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        print(f"ERRO DESCONHECIDO: {e}")  # ❌ Impossível rastrear em produção
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor...")  # ❌ Print ao invés de log
    uvicorn.run(app, host="0.0.0.0", port=8000)
