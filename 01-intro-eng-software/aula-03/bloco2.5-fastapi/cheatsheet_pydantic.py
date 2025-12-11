from pydantic import BaseModel, Field, validator
from typing import Optional

# ========================================
# VALIDAÇÕES BÁSICAS COM FIELD
# ========================================

class Usuario(BaseModel):
    # String com tamanho
    nome: str = Field(..., min_length=3, max_length=50)
    
    # Número com range
    idade: int = Field(..., ge=18, le=120)  # ge = greater or equal, le = less or equal
    
    # Float positivo
    salario: float = Field(..., gt=0)  # gt = greater than
    
    # Opcional com padrão
    ativo: bool = True
    
    # Opcional sem padrão
    apelido: Optional[str] = None

# ========================================
# VALIDAÇÕES COM VALIDATOR
# ========================================

class Produto(BaseModel):
    nome: str
    preco: float
    
    @validator('nome')
    def nome_maiusculo(cls, v):
        return v.upper()
    
    @validator('preco')
    def preco_positivo(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser positivo')
        return v

# ========================================
# EXEMPLOS DE CONSTRAINTS
# ========================================

class Exemplos(BaseModel):
    # Strings
    email: str = Field(..., min_length=5, max_length=100)
    senha: str = Field(..., min_length=8)
    
    # Números
    nota: float = Field(..., ge=0, le=10)  # Entre 0 e 10
    quantidade: int = Field(..., gt=0)      # Maior que 0
    desconto: float = Field(..., ge=0, lt=1)  # Entre 0 e 1 (exclusivo)
    
    # Boolean
    ativo: bool = True
    
    # Opcional
    observacao: Optional[str] = None

# ========================================
# TESTAR
# ========================================

if __name__ == "__main__":
    # Válido
    usuario = Usuario(nome="João Silva", idade=25, salario=5000.50)
    print(usuario.dict())
    
    # Inválido (descomente para ver erro)
    # usuario_invalido = Usuario(nome="Jo", idade=15, salario=-100)
