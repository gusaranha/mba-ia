from fastapi import FastAPI
from src.core.error_handlers import base_error_handler
from src.core.exceptions import BaseAPIError, BadRequestError
from src.core.middleware import RequestLoggingMiddleware
from src.api.v1.servidor_routes import router as servidor_routes_v1
from src.api.v1.error_routes import (router as error_routes_v1)

app = FastAPI(title="Gerenciador de tarefas")

# Middleware de logging
app.add_middleware(RequestLoggingMiddleware)

# Handlers de erro
app.add_exception_handler(BaseAPIError, base_error_handler)

# Rotas
app.include_router(servidor_routes_v1, prefix="/api/v1")
app.include_router(error_routes_v1, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok"}
