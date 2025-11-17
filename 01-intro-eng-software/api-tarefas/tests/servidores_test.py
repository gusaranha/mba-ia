from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_criar_servidor():
    payload = {"nome": "Joao da Silva", "carga_horaria": 40}
    response = client.post("/api/v1/servidores", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == "Joao da Silva"
    assert data["carga_horaria"] == 40


def test_listar_servidores():
    response = client.get("/api/v1/servidores")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_buscar_servidor():
    response = client.get("/api/v1/servidores/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_buscar_servidor_inexistente():
    response = client.get("/api/v1/servidores/999")
    assert response.status_code == 404