# bloco3-ml-fundamentos/api_regras.py

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Detecção de Fraude - Regras Manuais")

class Transacao(BaseModel):
    valor: float = Field(..., gt=0, description="Valor da transação em reais")
    hora: int = Field(..., ge=0, le=23, description="Hora da transação (0-23)")
    distancia_km: float = Field(..., ge=0, description="Distância da última compra em km")
    transacoes_hoje: int = Field(..., ge=1, description="Número de transações hoje")
    idade_conta_dias: int = Field(..., ge=0, description="Idade da conta em dias")

def detectar_fraude_regras(transacao: Transacao) -> dict:
    """
    Detecção de fraude usando REGRAS MANUAIS (if/else)
    
    Problema desta abordagem:
    - Regras fixas e inflexíveis
    - Não aprende com novos dados
    - Muitos falsos positivos/negativos
    - Difícil manutenção (muitas regras)
    """
    razoes = []
    
    # Regra 1: Valor muito alto
    if transacao.valor > 5000:
        razoes.append("Valor acima de R$ 5.000")
        return {
            "fraude": True,
            "confianca": 0.95,
            "metodo": "regras",
            "razoes": razoes
        }
    
    # Regra 2: Horário suspeito (madrugada)
    if transacao.hora >= 0 and transacao.hora <= 5:
        razoes.append("Transação na madrugada (0h-5h)")
        return {
            "fraude": True,
            "confianca": 0.85,
            "metodo": "regras",
            "razoes": razoes
        }
    
    # Regra 3: Distância muito grande
    if transacao.distancia_km > 1000:
        razoes.append("Distância maior que 1.000 km")
        return {
            "fraude": True,
            "confianca": 0.90,
            "metodo": "regras",
            "razoes": razoes
        }
    
    # Regra 4: Muitas transações no dia
    if transacao.transacoes_hoje > 10:
        razoes.append("Mais de 10 transações hoje")
        return {
            "fraude": True,
            "confianca": 0.80,
            "metodo": "regras",
            "razoes": razoes
        }
    
    # Regra 5: Conta muito nova
    if transacao.idade_conta_dias < 30:
        razoes.append("Conta com menos de 30 dias")
        return {
            "fraude": True,
            "confianca": 0.75,
            "metodo": "regras",
            "razoes": razoes
        }
    
    # Se não ativou nenhuma regra, considera legítima
    return {
        "fraude": False,
        "confianca": 0.70,
        "metodo": "regras",
        "razoes": ["Nenhuma regra de fraude ativada"]
    }

@app.get("/")
def raiz():
    return {
        "api": "Detecção de Fraude - Regras Manuais",
        "metodo": "if/else (programação tradicional)",
        "problema": "Regras fixas, não aprende com dados"
    }

@app.post("/analisar")
def analisar(transacao: Transacao):
    """
    Analisa transação usando REGRAS MANUAIS
    
    Limitações:
    - Regras são fixas (não evoluem)
    - Não considera combinações complexas
    - Falsos positivos: viagem legítima bloqueada
    - Falsos negativos: fraude nova não detectada
    """
    resultado = detectar_fraude_regras(transacao)
    
    return {
        "transacao": transacao.dict(),
        "resultado": resultado,
        "observacao": "⚠️ Este método usa regras fixas e não aprende com dados"
    }

# EXECUTAR:
# uvicorn api_regras:app --reload --port 8001
# Docs: http://localhost:8001/docs