"""
Testes Automatizados - API de Detecção de Fraude
Estrutura AAA: Arrange, Act, Assert
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


def test_root():
    """
    Teste: verificar endpoint raiz
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "versao" in data


def test_fraude_detectada_valor_alto():
    """
    Teste: transações acima de R$ 10.000 devem ser fraude
    Esta é a ESPECIFICAÇÃO da regra de negócio!
    """
    # ARRANGE (Preparar)
    payload = {
        "valor": 15000,  # Acima do threshold
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 50,
        "numero_transacoes_hoje": 3,
        "idade_conta_dias": 100
    }
    
    # ACT (Agir)
    response = client.post("/analisar", json=payload)
    
    # ASSERT (Verificar)
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == True  # ESPECIFICAÇÃO: > 10k = fraude
    assert data["confianca"] > 0.5
    assert "threshold" in data["motivo"].lower()


def test_transacao_legitima():
    """
    Teste: transações normais devem ser aprovadas
    """
    # ARRANGE
    payload = {
        "valor": 500,  # Abaixo do threshold
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 10,
        "numero_transacoes_hoje": 2,
        "idade_conta_dias": 100
    }
    
    # ACT
    response = client.post("/analisar", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == False
    assert data["confianca"] > 0.5


def test_fraude_horario_suspeito():
    """
    Teste: transações em horário suspeito (madrugada) devem ser fraude
    """
    # ARRANGE
    payload = {
        "valor": 500,
        "hora_do_dia": 3,  # 3h da manhã
        "distancia_ultima_compra_km": 10,
        "numero_transacoes_hoje": 1,
        "idade_conta_dias": 100
    }
    
    # ACT
    response = client.post("/analisar", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == True
    assert "horário" in data["motivo"].lower() or "suspeito" in data["motivo"].lower()


def test_fraude_distancia_grande():
    """
    Teste: transações com distância > 500km devem ser fraude
    """
    # ARRANGE
    payload = {
        "valor": 200,
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 850,  # Muito longe
        "numero_transacoes_hoje": 1,
        "idade_conta_dias": 100
    }
    
    # ACT
    response = client.post("/analisar", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == True
    assert "distância" in data["motivo"].lower() or "distancia" in data["motivo"].lower()


def test_valor_exato_threshold():
    """
    Teste de borda: valor exatamente no threshold
    """
    # ARRANGE
    payload = {
        "valor": 10000,  # Exatamente no limite
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 10,
        "numero_transacoes_hoje": 1,
        "idade_conta_dias": 100
    }
    
    # ACT
    response = client.post("/analisar", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    # No limite, não deve ser fraude (apenas > 10000)
    assert data["fraude"] == False
