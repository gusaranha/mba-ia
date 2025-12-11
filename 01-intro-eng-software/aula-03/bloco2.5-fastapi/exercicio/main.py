from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Exercício - API de Usuários")

# TODO 1: Criar classe Usuario com validação Pydantic
# Campos:
#   - nome: string, mínimo 3 caracteres
#   - email: string (não precisa validar formato por enquanto)
#   - idade: inteiro, entre 18 e 100
#   - ativo: boolean, padrão True


# TODO 2: Criar endpoint GET "/" que retorna info da API


# TODO 3: Criar endpoint POST "/usuarios" que recebe Usuario
# Deve retornar: {"mensagem": "...", "usuario": {...}}


# TODO 4: Criar endpoint GET "/usuarios/{usuario_id}"
# Deve retornar dados mockados do usuário


# TODO 5: Testar no Swagger (/docs) com casos válidos e inválidos
