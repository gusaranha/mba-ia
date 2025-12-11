from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    """Testa o endpoint de health check"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_calculo_soma():
    """Testa o cálculo (soma neste exemplo)"""
    payload = {
        "valor1": 10.0,
        "valor2": 20.0
    }
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    assert response.json()["resultado"] == 30.0

def test_calculo_negativos():
    """Testa o cálculo com valores negativos"""
    payload = {
        "valor1": -5.0,
        "valor2": 10.0
    }
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    assert response.json()["resultado"] == 5.0
