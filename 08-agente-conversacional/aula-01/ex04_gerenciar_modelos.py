# ex04_gerenciar_modelos.py
# Ex.04 Listar e Gerenciar Modelos com Python
# Objetivo: listar e comparar modelos disponíveis no Ollama
#
# Dependências:
#   pip install ollama
# (time é biblioteca padrão do Python, não precisa instalar)
# Requer também o servidor Ollama rodando localmente com os modelos
# "llama3" e "mistral" baixados (ollama pull llama3 / ollama pull mistral).

import ollama   # cliente do Ollama
import time     # para medir o tempo de resposta

# ─── Listar todos os modelos instalados ─────────────────────────
print("=== MODELOS INSTALADOS NO OLLAMA ===")
lista_modelos = ollama.list()    # retorna dicionário com chave "models"

for modelo in lista_modelos["models"]:
    # Cada "modelo" é um dicionário com: name, size, digest, modified_at
    nome      = modelo["name"]
    tamanho   = modelo.get("size", 0) / (1024**3)  # converte bytes → GB
    print(f"  • {nome:<30} {tamanho:.1f} GB")

# ─── Comparar velocidade de dois modelos ────────────────────────
print("\n=== COMPARAÇÃO DE VELOCIDADE ===")
PERGUNTA_TESTE = "Em uma frase: o que é uma delegacia de polícia?"

for nome_modelo in ["llama3", "mistral"]:
    try:
        inicio = time.time()  # registra o tempo antes da chamada

        resp = ollama.chat(
            model=nome_modelo,
            messages=[{"role": "user", "content": PERGUNTA_TESTE}],
            options={"temperature": 0, "num_predict": 50}
        )

        duracao = time.time() - inicio  # calcula o tempo decorrido
        tokens  = resp.get("eval_count", 0)  # tokens gerados

        print(f"\n  Modelo: {nome_modelo}")
        print(f"  Tempo:  {duracao:.2f}s")
        print(f"  Tokens: {tokens} ({tokens/duracao:.0f} tok/s)")
        print(f"  Resp:   {resp['message']['content'][:150]}")
    except Exception as e:
        print(f"  {nome_modelo}: não disponível ({e})")
