from pydantic import BaseModel

class FreteRequest(BaseModel):
    peso: float  # em kg
    distancia: int  # em km
    
    class Config:
        schema_extra = {
            "example": {
                "peso": 5.0,
                "distancia": 100
            }
        }

class FreteResponse(BaseModel):
    valor_frete: float
    
    class Config:
        schema_extra = {
            "example": {
                "valor_frete": 100.0
            }
        }
