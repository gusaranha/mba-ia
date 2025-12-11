from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
from datetime import datetime

app = FastAPI(
    title="API Demo - Bloco 2",
    description="Demonstração de login seguro e endpoints REST",
    version="1.0.0"
)

# CORS para permitir HTML local chamar API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de dados FAKE (apenas para demonstração)
USUARIOS_VALIDOS = {
    "admin": hashlib.sha256("senha123".encode()).hexdigest(),
    "joao": hashlib.sha256("abc456".encode()).hexdigest()
}


class Credenciais(BaseModel):
    usuario: str
    senha: str


class DadosTeste(BaseModel):
    nome: str
    valor: float


@app.get("/")
def raiz():
    return {
        "api": "Demo Bloco 2",
        "endpoints": {
            "login": "/login [POST]",
            "teste": "/teste-post [POST]"
        }
    }


@app.post("/login")
def login(credenciais: Credenciais):
    """Valida login - SEMPRE no backend"""
    senha_hash = hashlib.sha256(credenciais.senha.encode()).hexdigest()

    if USUARIOS_VALIDOS.get(credenciais.usuario) == senha_hash:
        return {
            "sucesso": True,
            "mensagem": "✅ Login válido!",
            "usuario": credenciais.usuario
        }

    raise HTTPException(status_code=401, detail="❌ Login inválido")


@app.post("/teste-post")
def teste_post(dados: DadosTeste):
    """Endpoint para testar POST sem autenticação"""
    return {
        "recebido": dados.dict(),
        "mensagem": "✅ POST funcionou!",
        "timestamp": datetime.now().isoformat()
    }
