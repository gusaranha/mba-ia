from pydantic import BaseModel

class ValidadorRequest(BaseModel):
    cpf: str
    
    class Config:
        schema_extra = {
            "example": {
                "cpf": "123.456.789-00"
            }
        }

class ValidadorResponse(BaseModel):
    cpf: str
    valido: bool
    
    class Config:
        schema_extra = {
            "example": {
                "cpf": "123.456.789-00",
                "valido": True
            }
        }
