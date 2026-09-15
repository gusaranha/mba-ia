from pydantic import BaseModel
from fastapi import FastAPI
from agents import Runner
from agente_1 import executar_agente
from agente_handoff_1 import executar_agente_handoff

app = FastAPI()


class Pergunta(BaseModel):
    mensagem: str


@app.get("/")
def inicio():
    return {
        "mensagem": "Olá mundo!"
    }


@app.post("/tools")
def perguntar_tools(pergunta: Pergunta):
    resultado = executar_agente(pergunta.mensagem)
    return {
        "pergunta": pergunta.mensagem,
        "mensagem": resultado
    }


@app.post("/handoff")
def perguntar_tools(pergunta: Pergunta):
    resultado = executar_agente_handoff(pergunta.mensagem)
    return {
        "pergunta": pergunta.mensagem,
        "mensagem": resultado
    }
