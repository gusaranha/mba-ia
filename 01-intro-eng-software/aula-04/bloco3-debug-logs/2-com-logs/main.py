"""
API de Detecção de Fraude - Versão COM LOGS ESTRUTURADOS
Este exemplo demonstra uma API que usa logging estruturado em JSON.
"""

import json
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import sys

# ✅ Configuração de logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def log_structured(level: str, event: str, **kwargs):
    """
    Função auxiliar para criar logs estruturados em JSON.
    
    ✅ Logs em JSON são:
    - Indexáveis (CloudWatch, Datadog, Elastic)
    - Consultáveis (queries complexas)
    - Alertáveis (triggers automáticos)
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "event": event,
        **kwargs
    }
    
    if level == "ERROR":
        logger.error(json.dumps(log_entry))
    elif level == "WARNING":
        logger.warning(json.dumps(log_entry))
    elif level == "INFO":
        logger.info(json.dumps(log_entry))
    else:
        logger.debug(json.dumps(log_entry))


app = FastAPI(
    title="API Detecção de Fraude - Com Logs",
    description="Exemplo de API com logging estruturado",
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
    log_structured("INFO", "health_check", endpoint="/")
    return {"status": "API Detecção de Fraude - Com Logs", "version": "1.0.0"}


@app.get("/health")
def health():
    log_structured("INFO", "health_check", endpoint="/health", status="healthy")
    return {"status": "healthy"}


@app.post("/analisar", response_model=TransacaoOutput)
def analisar_transacao(transacao: TransacaoInput, request: Request):
    """
    Analisa uma transação e retorna se é provável fraude.
    
    ✅ Esta versão usa logging estruturado em JSON.
    """
    
    # ✅ Log estruturado com contexto completo
    log_structured(
        "INFO",
        "transaction_received",
        valor=transacao.valor,
        hora_do_dia=transacao.hora_do_dia,
        client_ip=request.client.host if request.client else "unknown"
    )
    
    try:
        # Validação básica
        if transacao.valor <= 0:
            # ✅ Log de erro com contexto completo
            log_structured(
                "ERROR",
                "validation_failed",
                error_type="ValueError",
                error_message="Valor deve ser positivo",
                input_valor=transacao.valor
            )
            raise HTTPException(status_code=400, detail="Valor deve ser positivo")
        
        # Processamento
        valor_processado = transacao.valor
        
        # Lógica de detecção de fraude
        score_risco = 0.0
        regras_ativadas = []
        
        # Regra 1: Valor alto
        if transacao.valor > 10000:
            score_risco += 0.4
            regras_ativadas.append("valor_alto")
            # ✅ Log com contexto específico
            log_structured(
                "WARNING",
                "high_value_detected",
                valor=transacao.valor,
                threshold=10000,
                score_added=0.4
            )
        
        # Regra 2: Horário suspeito
        if transacao.hora_do_dia < 6 or transacao.hora_do_dia > 23:
            score_risco += 0.3
            regras_ativadas.append("horario_suspeito")
            # ✅ Log com contexto específico
            log_structured(
                "WARNING",
                "suspicious_hour_detected",
                hora_do_dia=transacao.hora_do_dia,
                score_added=0.3
            )
        
        # Regra 3: Distância grande
        if transacao.distancia_ultima_compra_km > 500:
            score_risco += 0.2
            regras_ativadas.append("distancia_grande")
            # ✅ Log com contexto específico
            log_structured(
                "WARNING",
                "large_distance_detected",
                distancia_km=transacao.distancia_ultima_compra_km,
                threshold=500,
                score_added=0.2
            )
        
        # Regra 4: Muitas transações
        if transacao.numero_transacoes_hoje > 10:
            score_risco += 0.1
            regras_ativadas.append("muitas_transacoes")
            # ✅ Log com contexto específico
            log_structured(
                "WARNING",
                "high_transaction_count",
                numero_transacoes=transacao.numero_transacoes_hoje,
                threshold=10,
                score_added=0.1
            )
        
        # Decisão
        fraude = score_risco >= 0.5
        
        if fraude:
            # ✅ Log estruturado de fraude detectada
            log_structured(
                "ERROR",
                "fraud_detected",
                score_risco=round(score_risco, 2),
                regras_ativadas=regras_ativadas,
                valor=transacao.valor,
                action="blocked"
            )
            mensagem = "Transação bloqueada por suspeita de fraude"
        else:
            # ✅ Log estruturado de transação aprovada
            log_structured(
                "INFO",
                "transaction_approved",
                score_risco=round(score_risco, 2),
                regras_ativadas=regras_ativadas,
                valor=transacao.valor,
                action="approved"
            )
            mensagem = "Transação aprovada"
        
        return TransacaoOutput(
            fraude=fraude,
            score_risco=round(score_risco, 2),
            valor_processado=valor_processado,
            mensagem=mensagem
        )
    
    except ValueError as e:
        # ✅ Log estruturado de erro de validação
        log_structured(
            "ERROR",
            "validation_error",
            error_type="ValueError",
            error_message=str(e),
            input_data=transacao.dict()
        )
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # ✅ Log estruturado de erro desconhecido
        log_structured(
            "ERROR",
            "unexpected_error",
            error_type=type(e).__name__,
            error_message=str(e),
            input_data=transacao.dict()
        )
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


if __name__ == "__main__":
    import uvicorn
    # ✅ Log estruturado de inicialização
    log_structured("INFO", "server_starting", host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
