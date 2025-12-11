from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_calculo_sem_cupom():
    payload = {
        "itens": [
            {"nome": "Mouse", "quantidade": 2, "preco": 50.0}
        ]
    }
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    assert response.json()["total"] == 100.0

def test_calculo_com_cupom():
    payload = {
        "itens": [
            {"nome": "Teclado", "quantidade": 1, "preco": 200.0}
        ],
        "cupom": "DESC10"
    }
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    assert response.json()["desconto"] == 20.0
    assert response.json()["total"] == 180.0

def test_multiplos_itens():
    payload = {
        "itens": [
            {"nome": "Mouse", "quantidade": 1, "preco": 50.0},
            {"nome": "Teclado", "quantidade": 1, "preco": 150.0}
        ]
    }
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    assert response.json()["subtotal"] == 200.0
