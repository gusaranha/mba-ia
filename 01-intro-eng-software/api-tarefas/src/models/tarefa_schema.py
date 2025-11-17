from pydantic import BaseModel, Field


class TarefaIn(BaseModel):
    descricao: str = Field(..., min_length=5, max_length=100, examples=["Verificar e-mails"])
    horas_execucao: int = Field(..., ge=1, le=10, examples=[2])
    responsavel_id: int = Field(..., ge=1, examples=[1])

class TarefaOut(TarefaIn):
    id: int = Field(..., examples=[1])