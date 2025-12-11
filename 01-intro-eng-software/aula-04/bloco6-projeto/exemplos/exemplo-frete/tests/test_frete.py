from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_calculo_frete_simples():
    payload = {"peso": 5.0, "distancia": 100}
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    # 5kg * 10 = 50 + 100km * 0.5 = 50 → Total: 100
    assert response.json()["valor_frete"] == 100.0

def test_calculo_frete_peso_alto():
    payload = {"peso": 10.0, "distancia": 50}
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    # 10kg * 10 = 100 + 50km * 0.5 = 25 → Total: 125
    assert response.json()["valor_frete"] == 125.0

def test_calculo_frete_distancia_longa():
    payload = {"peso": 2.0, "distancia": 500}
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    # 2kg * 10 = 20 + 500km * 0.5 = 250 → Total: 270
    assert response.json()["valor_frete"] == 270.0
