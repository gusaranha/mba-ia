# ex01_primeira_conversa.py
# Ex.01 Primeira conversa com o Llama 3 via Python
# Objetivo: primeira interação com o Llama 3 via Python
# Execute: python ex01_primeira_conversa.py
#
# Dependências:
#   pip install ollama
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama    # biblioteca que se comunica com o Ollama local

# ─── Chamada ao modelo ───────────────────────────────────────────
# ollama.chat() envia uma mensagem para o modelo e retorna a resposta
# Parâmetros:
#   model   → nome do modelo que queremos usar
#   messages → lista de mensagens no formato de chat
#              cada mensagem tem "role" (quem fala) e "content" (o que diz)
#              role pode ser: "system", "user", ou "assistant"
resposta = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "system",           # instrução para o modelo
            "content": "Você é um assistente da Polícia Civil do Brasil. "
                        "Responda sempre em português de forma profissional."
        },
        {
            "role": "user",             # mensagem do usuário
            "content": "Olá! Quais são suas principais funções?"
        }
    ]
)

# ─── Estrutura da resposta ───────────────────────────────────────
# resposta é um dicionário com várias chaves:
# resposta["message"]            → a mensagem gerada pelo modelo
# resposta["message"]["role"]    → quem gerou (sempre "assistant")
# resposta["message"]["content"] → o texto da resposta

print("=== RESPOSTA DO MODELO ===")
print(resposta["message"]["content"])

print("\n=== INFORMAÇÕES TÉCNICAS ===")
print(f"Modelo usado:     {resposta['model']}")
print(f"Tokens na entrada:{resposta['prompt_eval_count']}")
print(f"Tokens gerados:   {resposta['eval_count']}")
