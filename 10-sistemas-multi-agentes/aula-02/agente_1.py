from agents import Agent, Runner
from provedor import configurar

model = configurar()

agente = Agent(
    name="Meu Primeiro Agente",
    instructions="Você é um assistente útil e objetivo.",
    model=model,
)

def executar_agente(mensagem: str) -> str:
    resultado = Runner.run_sync(agente, mensagem)
    return resultado.final_output
