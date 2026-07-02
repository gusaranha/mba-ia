# ex03_conversa_multiturno.py
# Ex.03 Conversa com Múltiplos Turnos (Histórico)
# Objetivo: manter histórico de conversa entre múltiplas perguntas
#
# Dependências:
#   pip install ollama
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama

# O histórico é uma lista de mensagens acumuladas
# Cada nova pergunta e resposta é adicionada à lista
# O modelo recebe todo o histórico em cada chamada
historico = [
    {
        "role": "system",
        "content": ("Você é AgenteBO, assistente da Polícia Civil. "
                    "Especializado em legislação criminal e procedimentos policiais. "
                    "Sempre responda em português e de forma precisa.")
    }
]

# Simular uma conversa com 4 turnos
perguntas = [
    "Qual é a diferença entre furto e roubo?",
    "Quais são as penas previstas para cada um?",
    "E quando há violência no furto, muda a tipificação?",
    "Cite o artigo do Código Penal que trata disso.",
]

for pergunta in perguntas:
    print(f"\n👤 USUÁRIO: {pergunta}")

    # Adiciona a pergunta do usuário ao histórico
    historico.append({
        "role": "user",
        "content": pergunta
    })

    # Envia o histórico COMPLETO ao modelo
    # Isso é o que permite ao modelo "lembrar" o contexto anterior
    resposta = ollama.chat(
        model="llama3",
        messages=historico,          # envia toda a conversa até agora
        options={"temperature": 0.1} # baixa temperatura para respostas precisas
    )

    # Extrai o texto da resposta
    texto_resposta = resposta["message"]["content"]

    # Adiciona a resposta do assistente ao histórico
    historico.append({
        "role": "assistant",
        "content": texto_resposta
    })

    print(f"🤖 AGENTE: {texto_resposta[:300]}...")

print(f"\nTotal de mensagens no histórico: {len(historico)}")
print(f"(1 system + {len(perguntas)} perguntas + {len(perguntas)} respostas)")
