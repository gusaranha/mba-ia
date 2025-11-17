from fastapi import APIRouter
from src.core.logger import log
from src.models.schemas import ServidorIn, ServidorOut
from src.repositories.servidor import servidor_repo
from src.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError

router = APIRouter(prefix="/servidores", tags=["Servidores"])

@router.get("/", response_model=list[ServidorOut])
def listar_servidores():
    return servidor_repo.find()


@router.get("/{servidor_id}", response_model=ServidorOut)
def buscar_servidor(servidor_id: int):
    servidor = servidor_repo.get(servidor_id)
    if not servidor:
        raise NotFoundError(status_code=404, detail="Servidor não encontrado")
    return servidor


@router.post("/", response_model=ServidorOut, status_code=201)
def adicionar_servidor(data: ServidorIn):
    return servidor_repo.add(data)


@router.delete("/{servidor_id}", status_code=204)
def deletar(servidor_id: int):
    servidor = servidor_repo.get(servidor_id)
    if not servidor:
        raise NotFoundError(status_code=404, detail="Servidor não encontrado")
    servidor_repo.delete(servidor_id)
    return None