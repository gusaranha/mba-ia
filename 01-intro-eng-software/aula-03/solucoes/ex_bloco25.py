from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Exercício - API de Usuários")

# SOLUÇÃO TODO 1: Criar classe Usuario com validação Pydantic
class Usuario(BaseModel):
    # Field(...) marca campo como obrigatório
    # min_length=3 garante que nome tem pelo menos 3 caracteres
    nome: str = Field(..., min_length=3, max_length=100, description="Nome do usuário")
    
    # Email como string simples (validação básica)
    email: str = Field(..., description="Email do usuário")
    
    # ge=18 (greater or equal) e le=100 (less or equal) definem range
    idade: int = Field(..., ge=18, le=100, description="Idade entre 18 e 100 anos")
    
    # Campo opcional com valor padrão True
    # Se não enviar no JSON, assume True automaticamente
    ativo: bool = True


# SOLUÇÃO TODO 2: Criar endpoint GET "/" que retorna info da API
@app.get("/")
def raiz():
    """
    Endpoint raiz - convenção para informar sobre a API
    Retorna dict que FastAPI converte automaticamente para JSON
    """
    return {
        "api": "Sistema de Usuários",
        "versao": "1.0.0",
        "endpoints": {
            "documentacao": "/docs",
            "criar_usuario": "/usuarios [POST]",
            "obter_usuario": "/usuarios/{usuario_id} [GET]"
        }
    }


# SOLUÇÃO TODO 3: Criar endpoint POST "/usuarios" que recebe Usuario
@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    """
    Recebe objeto Usuario no body da requisição
    Pydantic valida automaticamente:
    - Se todos campos obrigatórios estão presentes
    - Se tipos estão corretos (str, int, bool)
    - Se valores respeitam constraints (min_length, ge, le)
    
    Se validação falhar, FastAPI retorna erro 422 automaticamente
    Se passar, objeto usuario já vem validado e pronto para usar
    """
    return {
        "mensagem": f"Usuário {usuario.nome} criado com sucesso!",
        "usuario": usuario.dict(),  # Converte Pydantic model para dict
        "status": "ativo" if usuario.ativo else "inativo"
    }


# SOLUÇÃO TODO 4: Criar endpoint GET "/usuarios/{usuario_id}"
@app.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int):
    """
    Path parameter {usuario_id} é capturado da URL
    FastAPI converte automaticamente para int
    Se enviar letra, retorna erro 422
    
    Em produção real, buscaria usuário no banco de dados
    Aqui retornamos dados mockados para demonstração
    """
    # Dados mockados (fake)
    return {
        "usuario_id": usuario_id,
        "nome": "João Silva",
        "email": "joao@email.com",
        "idade": 25,
        "ativo": True
    }


# SOLUÇÃO TODO 5: Testar no Swagger (/docs)
"""
CASOS DE TESTE:

1. CASO VÁLIDO:
POST /usuarios
{
  "nome": "Maria Santos",
  "email": "maria@email.com",
  "idade": 30,
  "ativo": true
}
✅ Retorna 200 com dados do usuário


2. CASO INVÁLIDO - Nome curto:
{
  "nome": "Jo",
  "email": "jo@email.com",
  "idade": 25
}
❌ Erro 422: "ensure this value has at least 3 characters"


3. CASO INVÁLIDO - Idade menor que 18:
{
  "nome": "Pedro Costa",
  "email": "pedro@email.com",
  "idade": 15
}
❌ Erro 422: "ensure this value is greater than or equal to 18"


4. CASO INVÁLIDO - Idade maior que 100:
{
  "nome": "Ana Lima",
  "email": "ana@email.com",
  "idade": 150
}
❌ Erro 422: "ensure this value is less than or equal to 100"


5. CASO INVÁLIDO - Campo faltando:
{
  "nome": "Carlos Souza",
  "idade": 28
}
❌ Erro 422: "field required" (email está faltando)


6. CASO VÁLIDO - Sem campo opcional:
{
  "nome": "Fernanda Dias",
  "email": "fernanda@email.com",
  "idade": 35
}
✅ Retorna 200 (ativo assume True automaticamente)


7. GET /usuarios/123
✅ Retorna 200 com dados mockados


8. GET /usuarios/abc
❌ Erro 422: "value is not a valid integer"
"""

# EXECUTAR:
# uvicorn solucao_exercicio_bloco2.5:app --reload
# Acessar: http://localhost:8000/docs