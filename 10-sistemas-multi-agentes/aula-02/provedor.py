import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

load_dotenv()


def configurar():
    cliente = AsyncOpenAI(
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY"),
    )

    set_default_openai_client(cliente)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)

    return os.getenv("LLM_MODEL")


async def main():
    model = configurar()

    agent = Agent(
        name="Assistente",
        instructions="Você é um assistente útil e objetivo.",
        model=model,
    )

    result = await Runner.run(
        agent,
        "Explique em uma frase o que é RAG."
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
