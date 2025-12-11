from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()

# ========================================
# SCHEMAS PYDANTIC
# ========================================

class Item(BaseModel):
    nome: str
    preco: float
    ativo: bool = True  # Campo opcional com padrão

# ========================================
# ENDPOINTS BÁSICOS
# ========================================

@app.get("/")
def raiz():
    return {"mensagem": "API funcionando"}

# Path parameter
@app.get("/items/{item_id}")
def obter_item(item_id: int):
    return {"item_id": item_id}

# Query parameters
@app.get("/buscar")
def buscar(q: str = None, limite: int = 10):
    return {"query": q, "limite": limite}

# Query com validação
@app.get("/buscar-validado")
def buscar_validado(
    q: str = Query(..., min_length=3),
    limite: int = Query(10, le=100)
):
    return {"query": q, "limite": limite}

# POST com body
@app.post("/items")
def criar_item(item: Item):
    return {"criado": item.dict()}

# PUT
@app.put("/items/{item_id}")
def atualizar_item(item_id: int, item: Item):
    return {"atualizado": item_id, "dados": item.dict()}

# DELETE
@app.delete("/items/{item_id}")
def deletar_item(item_id: int):
    return {"deletado": item_id}

# ========================================
# EXECUTAR
# ========================================
# uvicorn cheatsheet_fastapi:app --reload
# Docs: http://localhost:8000/docs
