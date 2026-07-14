# ex06_funcoes_base.py
# Ex.06 Criar uma função Python reutilizável para o Agente.
#
# Dependências:
#   pip install ollama
# (json e typing são bibliotecas padrão do Python, não precisam ser instaladas)
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama
import json
from typing import Optional    # para tipagem opcional

# ─── Função 1: chat simples ──────────────────────────────────────
def chat(mensagem: str,
         modelo: str = "llama3",
         temperatura: float = 0.1,
         sistema: Optional[str] = None) -> str:
    """
    Envia uma mensagem ao LLM e retorna a resposta como string.

    Parâmetros:
        mensagem:    texto do usuário
        modelo:      nome do modelo Ollama (padrão: llama3)
        temperatura: criatividade do modelo (0=determinístico, 1=criativo)
        sistema:     instrução de sistema (persona do assistente)

    Retorna:
        texto da resposta do modelo
    """
    mensagens = []

    # Adiciona instrução de sistema se fornecida
    if sistema:
        mensagens.append({"role": "system", "content": sistema})

    # Adiciona a mensagem do usuário
    mensagens.append({"role": "user", "content": mensagem})

    # Faz a chamada ao Ollama
    resposta = ollama.chat(
        model=modelo,
        messages=mensagens,
        options={"temperature": temperatura}
    )

    # Retorna apenas o texto da resposta
    return resposta["message"]["content"]


# ─── Função 2: chat com saída JSON ──────────────────────────────
def chat_json(mensagem: str,
              modelo: str = "llama3",
              sistema: Optional[str] = None) -> dict:
    """
    Envia uma mensagem ao LLM e retorna a resposta como dicionário.
    Garante retorno em JSON válido usando format="json".

    Retorna:
        dicionário Python com os dados extraídos
        dicionário vazio em caso de erro
    """
    mensagens = []
    if sistema:
        mensagens.append({"role": "system", "content": sistema})
    mensagens.append({"role": "user", "content": mensagem})

    resposta = ollama.chat(
        model=modelo,
        messages=mensagens,
        format="json",               # força JSON válido
        options={"temperature": 0}   # temperatura 0 para JSON confiável
    )

    try:
        return json.loads(resposta["message"]["content"])
    except json.JSONDecodeError:
        return {}  # retorna dicionário vazio se JSON inválido


# ─── Testes das funções ─────────────────────────────────────────
if __name__ == "__main__":
    # Teste 1: chat simples
    print("=== TESTE 1: CHAT SIMPLES ===")
    SISTEMA_POLICIAL = ("Você é um assistente jurídico da Polícia Civil. "
                        "Responda de forma concisa e técnica.")

    resposta = chat(
        mensagem="O que é o flagrante delito?",
        sistema=SISTEMA_POLICIAL
    )
    print(resposta)

    # Teste 2: extração de JSON
    print("\n=== TESTE 2: EXTRAÇÃO DE DADOS EM JSON ===")
    dados = chat_json(
        mensagem=("Extraia em JSON: vitima, crime, local. "
                  "Texto: 'Maria sofreu furto de bolsa na Av. Paulista.'")
    )
    print(json.dumps(dados, ensure_ascii=False, indent=2))
