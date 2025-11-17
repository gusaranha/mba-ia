from pydantic import BaseModel, Field


class ServidorIn(BaseModel):
    nome: str = Field(..., min_length=5, max_length=100, examples=["Fulano de Tal"])
    carga_horaria: int = Field(..., ge=20, le=80, examples=[20])

class ServidorOut(ServidorIn):
    id: int = Field(..., examples=[1])