# ex05_processar_documento.py
# Ex.05 Lendo e Processando Arquivos de Texto
#
# Dependências:
#   pip install ollama
# (json é biblioteca padrão do Python, não precisa instalar)
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama
import json   # para trabalhar com dados estruturados

# ─── Criar um BO fictício para teste ────────────────────────────
# Em produção, este texto viria de um arquivo real
BO_FICTICIO = """
BOLETIM DE OCORRÊNCIA Nº 2025/004521
Data: 15/03/2025  Hora: 14h32  Delegacia: 1ª DP - Centro
Natureza: Furto (Art. 155 CP)

Vítima: João Carlos Pereira, 34 anos, RG 12.345.678-9
Endereço: Rua das Flores, 123, Apto 45 - Jardim Primavera

Relato: O declarante informa que deixou seu veículo, um Chevrolet Onix
2022, placas ABC-1234, cor prata, estacionado na Rua XV de Novembro
às 13h00. Ao retornar às 14h20 constatou o desaparecimento do aparelho
celular iPhone 15 Pro Max que estava no banco do passageiro.
Valor estimado do bem: R$ 8.500,00.
Suspeitos: não identificados.
"""

# Salvar o BO em arquivo (simulando um arquivo real)
with open("bo_teste.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(BO_FICTICIO)

# ─── Ler o arquivo ───────────────────────────────────────────────
# Em produção, leria o BO do sistema de gestão
with open("bo_teste.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()

# ─── Extrair informações com o LLM ──────────────────────────────
prompt = f"""Analise o boletim de ocorrência abaixo e extraia as informações
em formato JSON com os seguintes campos:
- numero_bo: número do boletim
- data: data da ocorrência
- natureza: tipo de crime
- artigo_cp: artigo do Código Penal
- vitima: nome da vítima
- bem_subtraido: descrição do bem
- valor: valor em reais
- local: local do crime

Retorne APENAS o JSON, sem explicações.

Boletim:
{conteudo}
"""

resposta = ollama.chat(
    model="llama3",
    messages=[{"role": "user", "content": prompt}],
    format="json",           # força retorno em JSON válido
    options={"temperature": 0}  # temperatura 0 para precisão máxima
)

# ─── Processar o JSON retornado ─────────────────────────────────
try:
    dados = json.loads(resposta["message"]["content"])
    print("=== DADOS EXTRAÍDOS DO BO ===")
    for chave, valor in dados.items():
        print(f"  {chave:<20}: {valor}")
except json.JSONDecodeError as e:
    print(f"Erro ao parsear JSON: {e}")
    print("Resposta bruta:", resposta["message"]["content"])
