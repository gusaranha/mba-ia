from fastapi import FastAPI
from src.core.error_handlers import base_error_handler
from src.core.exceptions import BaseAPIError, BadRequestError
from src.core.middleware import RequestLoggingMiddleware
from src.core.logger import log

app = FastAPI(title="Gerenciador de tarefas")

# Middleware de logging
app.add_middleware(RequestLoggingMiddleware)

# Handlers de erro
app.add_exception_handler(BaseAPIError, base_error_handler)


@app.get("/")
def health_check():
    log("INFO", "health_check", endpoint="/")
    return {"status": "ok"}


@app.get("/exception")
def health_check():
    raise BadRequestError("Invalid parameters", field="name")