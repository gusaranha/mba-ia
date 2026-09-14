import os
from agents import Agent, Runner, set_default_openai_key
from provedor import configurar

configurar()

agente = Agent(
    name="Primeiro agente",
    instructions="Você é um agente de teste. Responda Olá mundo!",
    model=os.getenv("OPENAI_DEFAULT_MODEL", "llama3.1")
)

resultado = Runner.run_sync(
    agente,
    "O que vce faz?"
)

print(resultado)

print("O agente que respondeu: ", agente.name)
print("Resposta final: ", resultado.final_output)


