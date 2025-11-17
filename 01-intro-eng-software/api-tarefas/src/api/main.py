from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gerenciador de tarefas")

@app.get("/")
def health_check():
    logger.info("Health check")
    return {"status": "ok"}