from fastapi.testclient import TestClient
from src.api.main import app
import logging

client = TestClient(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_criar():
    payload = {"nome": "Joao da Silva", "carga_horaria": 40}
    response = client.post("/api/v1/servidores", json = payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["nome"] == "Joao da Silva"
    assert data["carga_horaria"] == 40


def test_listares():
    response = client.get("/api/v1/servidores")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_buscar():
    response = client.get("/api/v1/servidores/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None


def test_buscar_inexistente():
    response = client.get("/api/v1/servidores/999")
    assert response.status_code == 404


def test_deletar():
    response = client.delete("/api/v1/servidores/1")
    assert response.status_code == 204


def test_tarefas():
    payload = {"nome": "Fulano de Tal", "carga_horaria": 10}
    response = client.post("/api/v1/servidores", json = payload)
    assert response.status_code == 201
    servidor_id = response.json()["id"]

    # nenhuma tarefa designada
    response = client.get(f"/api/v1/servidores/{servidor_id}/tarefas")
    assert response.status_code == 200
    data = response.json()
    assert data["servidor"]["id"] == servidor_id
    assert len(data["tarefas_designadas"]) == 0
    assert data["horas_disponiveis"] == 10
    assert data["porcentagem_ocupacao"] == 0

    # designa tarefa de 2h
    payload = {"descricao": "Responder e-mails", "horas_execucao": 2, "responsavel_id": servidor_id}
    response = client.post("/api/v1/tarefas", json = payload)
    assert response.status_code == 201

    # 1 tarefa - 2h designadas
    response = client.get(f"/api/v1/servidores/{servidor_id}/tarefas")
    assert response.status_code == 200
    data = response.json()
    assert data["servidor"]["id"] == servidor_id
    assert len(data["tarefas_designadas"]) == 1
    assert data["horas_disponiveis"] == 8
    assert data["porcentagem_ocupacao"] == 20

    # designa tarefa de 3h
    payload = {"descricao": "Deploy em produção", "horas_execucao": 3, "responsavel_id": servidor_id}
    response = client.post("/api/v1/tarefas", json = payload)
    assert response.status_code == 201

    # 2 tarefas - 5h designadas
    response = client.get(f"/api/v1/servidores/{servidor_id}/tarefas")
    assert response.status_code == 200
    data = response.json()
    assert data["servidor"]["id"] == servidor_id
    assert len(data["tarefas_designadas"]) == 2
    assert data["horas_disponiveis"] == 5
    assert data["porcentagem_ocupacao"] == 50

    # designa tarefa de 7h
    payload = {"descricao": "Follow up no cliente", "horas_execucao": 7, "responsavel_id": servidor_id}
    response = client.post("/api/v1/tarefas", json = payload)
    assert response.status_code == 201

    # 3 tarefas - 12h designadas
    response = client.get(f"/api/v1/servidores/{servidor_id}/tarefas")
    assert response.status_code == 200
    data = response.json()
    assert data["servidor"]["id"] == servidor_id
    assert len(data["tarefas_designadas"]) == 3
    assert data["horas_disponiveis"] == 0
    assert data["porcentagem_ocupacao"] == 100