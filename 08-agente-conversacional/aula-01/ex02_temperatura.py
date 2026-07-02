# ex02_temperatura.py
# Ex.02 Explorando parâmetros de temperatura
# Objetivo: comparar respostas com diferentes temperaturas
# A temperatura controla a "criatividade" do modelo:
#   0.0 → sempre escolhe o token mais provável (determinístico)
#   0.5 → equilíbrio entre consistência e variação
#   1.0 → alta variação, mais criativo mas menos consistente
#
# Dependências:
#   pip install ollama
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama

PERGUNTA = ("Escreva em 2 frases a definição de 'suspeito' "
            "para uso em investigação policial.")

# Testar três temperaturas diferentes
for temperatura in [0.0, 0.5, 1.0]:
    separador = "=" * 50
    print(f"\n{separador}")
    print(f"TEMPERATURA: {temperatura}")
    print("="*50)

    # Fazemos 2 chamadas com a mesma temperatura para ver a variação
    for i in range(2):
        resposta = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": PERGUNTA}],
            options={
                "temperature": temperatura,  # controla a variação da resposta
                "num_predict": 100,          # limita a resposta a ~100 tokens
            }
        )
        print(f"\nChamada {i+1}:")
        print(resposta["message"]["content"])

# Observação esperada:
# temperatura=0.0 → as 2 chamadas produzem textos idênticos ou muito similares
# temperatura=1.0 → cada chamada produz um texto diferente
