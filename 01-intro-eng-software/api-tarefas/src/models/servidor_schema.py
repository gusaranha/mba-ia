from pydantic import BaseModel, Field
from src.models.tarefa_schema import TarefaOut
from typing import List


class ServidorIn(BaseModel):
    nome: str = Field(..., min_length=5, max_length=100, examples=["Fulano de Tal"])
    carga_horaria: int = Field(..., ge=10, le=80, examples=[20])


class ServidorOut(ServidorIn):
    id: int = Field(..., examples=[1])


class ServidorTarefas(BaseModel):
    servidor: ServidorOut
    tarefas_designadas: List["TarefaOut"]
    horas_disponiveis: int
    porcentagem_ocupacao: int