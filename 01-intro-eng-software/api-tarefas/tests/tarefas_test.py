from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_criar():
    payload = {"descricao": "Responder e-mails", "horas_execucao": 2, "responsavel_id": 1}
    response = client.post("/api/v1/tarefas", json = payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["descricao"] == "Responder e-mails"
    assert data["horas_execucao"] == 2
    assert data["responsavel_id"] == 1


def test_listar():
    response = client.get("/api/v1/tarefas")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_buscar():
    response = client.get("/api/v1/tarefas/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None


def test_buscar_inexistente():
    response = client.get("/api/v1/tarefas/999")
    assert response.status_code == 404

def test_deletar():
    response = client.delete("/api/v1/tarefas/1")
    assert response.status_code == 204