from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_cpf_valido_formatado():
    payload = {"cpf": "123.456.789-00"}
    response = client.post("/validar", json=payload)
    assert response.status_code == 200
    assert response.json()["valido"] == True

def test_cpf_valido_sem_formatacao():
    payload = {"cpf": "12345678900"}
    response = client.post("/validar", json=payload)
    assert response.status_code == 200
    assert response.json()["valido"] == True

def test_cpf_invalido_curto():
    payload = {"cpf": "123"}
    response = client.post("/validar", json=payload)
    assert response.status_code == 200
    assert response.json()["valido"] == False

def test_cpf_invalido_com_letras():
    payload = {"cpf": "123.456.789-AB"}
    response = client.post("/validar", json=payload)
    assert response.status_code == 200
    assert response.json()["valido"] == False
