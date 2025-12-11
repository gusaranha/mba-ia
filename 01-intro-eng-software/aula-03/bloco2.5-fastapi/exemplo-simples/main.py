from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Exemplo Simples - Validação Pydantic")

# Schema com validação
class Produto(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50)
    preco: float = Field(..., gt=0, description="Preço deve ser positivo")
    estoque: int = Field(..., ge=0, description="Estoque não pode ser negativo")
    ativo: bool = True

@app.get("/")
def raiz():
    return {"mensagem": "API de Produtos", "docs": "/docs"}

@app.post("/produtos")
def criar_produto(produto: Produto):
    return {
        "mensagem": "Produto criado com sucesso!",
        "produto": produto.dict(),
        "preco_formatado": f"R$ {produto.preco:.2f}"
    }

@app.get("/produtos/{produto_id}")
def obter_produto(produto_id: int):
    return {
        "produto_id": produto_id,
        "nome": "Produto Exemplo",
        "preco": 99.90
    }
