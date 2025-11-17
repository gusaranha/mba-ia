from fastapi import APIRouter
from src.core.logger import log
from src.models.servidor_schema import ServidorIn, ServidorOut, ServidorTarefas
from src.repositories.servidor_repo import servidor_repo
from src.repositories.tarefa_repo import tarefa_repo
from src.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError

router = APIRouter(prefix="/servidores", tags=["Servidores"])

@router.get("/", response_model=list[ServidorOut])
def find():
    return servidor_repo.find()


@router.get("/{servidor_id}", response_model=ServidorOut)
def get(servidor_id: int):
    servidor = servidor_repo.get(servidor_id)
    if not servidor:
        raise NotFoundError(detail="Servidor não encontrado")
    return servidor


@router.post("/", response_model=ServidorOut, status_code=201)
def create(data: ServidorIn):
    if data.carga_horaria == 0:
        raise BadRequestError(detail="Carga horária do servidor deve ser maior que zero")

    return servidor_repo.add(data)


@router.delete("/{servidor_id}", status_code=204)
def delete(servidor_id: int):
    servidor = servidor_repo.get(servidor_id)
    if not servidor:
        raise NotFoundError(detail="Servidor não encontrado")

    servidor_repo.delete(servidor_id)
    return None


@router.get("/{servidor_id}/tarefas", response_model=ServidorTarefas)
def get_tarefas(servidor_id: int):
    servidor = servidor_repo.get(servidor_id)
    if not servidor:
        raise NotFoundError(detail="Servidor não encontrado")

    if servidor.carga_horaria == 0:
        raise BadRequestError(detail="Carga horária do servidor inválida")

    tarefas = tarefa_repo.find_by_servidor(servidor_id)
    horas_tarefas = sum(t.horas_execucao for t in tarefas)
    horas_disponiveis = servidor.carga_horaria - horas_tarefas
    porcentagem_ocupacao = horas_tarefas / servidor.carga_horaria * 100

    if horas_disponiveis < 0:
        horas_disponiveis = 0
        porcentagem_ocupacao = 100

    return ServidorTarefas(
        servidor = servidor,
        tarefas_designadas = tarefas,
        horas_disponiveis = horas_disponiveis,
        porcentagem_ocupacao = porcentagem_ocupacao
    )
