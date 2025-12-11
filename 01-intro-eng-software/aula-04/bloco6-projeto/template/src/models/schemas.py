from pydantic import BaseModel

class CalculoRequest(BaseModel):
    """
    Modelo de entrada - ADAPTE para seu projeto!
    """
    valor1: float
    valor2: float
    
    class Config:
        schema_extra = {
            "example": {
                "valor1": 10.0,
                "valor2": 20.0
            }
        }

class CalculoResponse(BaseModel):
    """
    Modelo de saída - ADAPTE para seu projeto!
    """
    resultado: float
    
    class Config:
        schema_extra = {
            "example": {
                "resultado": 30.0
            }
        }
