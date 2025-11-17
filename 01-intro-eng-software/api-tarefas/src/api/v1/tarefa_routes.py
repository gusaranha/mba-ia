from fastapi import APIRouter
from src.core.logger import log
from src.models.tarefa_schema import TarefaIn, TarefaOut
from src.repositories.tarefa import tarefa_repo
from src.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])

@router.get("/", response_model=list[TarefaIn])
def find():
    return tarefa_repo.find()


@router.get("/{tarefa_id}", response_model=TarefaOut)
def get(tarefa_id: int):
    tarefa = tarefa_repo.get(tarefa_id)
    if not tarefa:
        raise NotFoundError(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@router.post("/", response_model=TarefaOut, status_code=201)
def create(data: TarefaIn):
    return tarefa_repo.add(data)


@router.delete("/{tarefa_id}", status_code=204)
def delete(tarefa_id: int):
    servidor = tarefa_repo.get(tarefa_id)
    if not servidor:
        raise NotFoundError(status_code=404, detail="Tarefa não encontrada")
    tarefa_repo.delete(tarefa_id)
    return None