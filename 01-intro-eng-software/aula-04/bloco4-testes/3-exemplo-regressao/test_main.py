"""
Testes - Exemplo de Regressão
Estes testes vão PASSAR com main_correto.py
Mas vão FALHAR com main_quebrado.py (detectando a regressão!)
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """
    Teste básico: verificar se a API está funcionando
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_fraude_detectada_valor_alto():
    """
    🛡️ TESTE CRÍTICO - Campo de Força!
    
    ESPECIFICAÇÃO: Transações > R$ 10.000 DEVEM ser fraude
    
    Este teste vai FALHAR se alguém mudar o threshold para R$ 15.000,
    detectando a regressão automaticamente!
    """
    # ARRANGE
    payload = {
        "valor": 15000,  # R$ 15.000 - acima do threshold de R$ 10k
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 50,
        "numero_transacoes_hoje": 3,
        "idade_conta_dias": 100
    }
    
    # ACT
    response = client.post("/analisar", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    
    # 🔴 ESTE ASSERT VAI FALHAR na versão quebrada!
    # Versão correta: fraude=True (threshold 10k)
    # Versão quebrada: fraude=False (threshold mudou para 15k)
    assert data["fraude"] == True, \
        f"REGRESSÃO DETECTADA! R$ 15.000 deveria ser fraude, mas retornou {data}"


def test_transacao_legitima():
    """
    Teste: transações pequenas devem ser aprovadas
    """
    payload = {
        "valor": 500,
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 10,
        "numero_transacoes_hoje": 2,
        "idade_conta_dias": 100
    }
    
    response = client.post("/analisar", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == False


def test_valor_limite_superior():
    """
    🛡️ TESTE DE BORDA - Campo de Força!
    
    R$ 12.000 está acima do threshold de R$ 10.000
    Deve ser detectado como fraude
    
    Este teste também vai FALHAR na versão quebrada
    """
    payload = {
        "valor": 12000,  # Entre 10k e 15k
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 50,
        "numero_transacoes_hoje": 2,
        "idade_conta_dias": 100
    }
    
    response = client.post("/analisar", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # 🔴 ESTE ASSERT VAI FALHAR na versão quebrada!
    assert data["fraude"] == True, \
        f"REGRESSÃO DETECTADA! R$ 12.000 deveria ser fraude, mas retornou {data}"


def test_valor_exatamente_10k():
    """
    Teste de borda: valor exatamente R$ 10.000
    Não deve ser fraude (apenas > 10000)
    """
    payload = {
        "valor": 10000,
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 10,
        "numero_transacoes_hoje": 1,
        "idade_conta_dias": 100
    }
    
    response = client.post("/analisar", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == False
