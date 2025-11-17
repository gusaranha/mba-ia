from fastapi import FastAPI
from src.logger import log_structured

app = FastAPI(title="Gerenciador de tarefas")

@app.get("/")
def health_check():
    log_structured("INFO", "health_check", endpoint="/")
    return {"status": "ok"}