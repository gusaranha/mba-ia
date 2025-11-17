from fastapi import FastAPI
from src.core.error_handlers import base_error_handler
from src.core.exceptions import BaseAPIError, BadRequestError
from src.core.middleware import RequestLoggingMiddleware
from src.api.v1.routes import router as v1_router
from src.api.v1.error import router as error_router

app = FastAPI(title="Gerenciador de tarefas")

# Middleware de logging
app.add_middleware(RequestLoggingMiddleware)

# Handlers de erro
app.add_exception_handler(BaseAPIError, base_error_handler)

# Rotas
app.include_router(v1_router, prefix="/api/v1")
app.include_router(error_router, prefix="/api/error")

@app.get("/")
def health_check():
    return {"status": "ok"}
