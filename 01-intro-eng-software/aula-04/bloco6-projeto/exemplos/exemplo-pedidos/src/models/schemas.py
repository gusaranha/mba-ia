from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    nome: str
    quantidade: int
    preco: float

class PedidoRequest(BaseModel):
    itens: List[Item]
    cupom: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "itens": [
                    {"nome": "Mouse", "quantidade": 2, "preco": 50.0}
                ],
                "cupom": "DESC10"
            }
        }

class PedidoResponse(BaseModel):
    subtotal: float
    desconto: float
    total: float
