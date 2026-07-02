# ex07_classificador_bo.py
# Ex.07 Classificador de boletins de ocorrência
#
# Dependências:
#   pip install ollama
# (json é biblioteca padrão do Python, não precisa instalar)
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama
import json

# ─── Tipos de crime para classificação ──────────────────────────
TIPOS_CRIME = [
    "Furto",
    "Roubo",
    "Estelionato",
    "Ameaça",
    "Lesão Corporal",
    "Tráfico de Drogas",
    "Crime Digital",
    "Outros",
]

# ─── BOs para classificação ─────────────────────────────────────
BOS_TESTE = [
    "Vítima relata que foi abordada por dois indivíduos armados que levaram seu celular e carteira.",
    "Declarante informa que comprou produto pela internet mas nunca recebeu e o vendedor não atende.",
    "Vítima recebeu mensagens ameaçadoras de seu ex-companheiro pelo WhatsApp.",
    "Furto de notebook do interior de veículo estacionado.",
]

# ─── Função classificadora ──────────────────────────────────────
def classificar_bo(relato: str) -> dict:
    """
    Classifica um boletim de ocorrência por tipo de crime.

    Parâmetros:
        relato: texto descritivo do BO
    Retorna:
        dicionário com tipo, artigo CP, urgência e resumo
    """
    tipos_str = ", ".join(TIPOS_CRIME)  # converte lista em texto

    prompt = f"""Você é um delegado experiente da Polícia Civil.
Analise o relato abaixo e classifique o crime.

Tipos disponíveis: {tipos_str}

Retorne JSON com:
- tipo: o tipo do crime (exatamente como listado acima)
- artigo_cp: artigo do Código Penal ou Código Penal Militar
- urgencia: ALTA, MEDIA ou BAIXA
- resumo: resumo em 1 frase
- flagrante: true ou false (há possibilidade de flagrante?)

Relato: {relato}
"""

    resposta = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0}  # temperatura 0 para classificação precisa
    )

    try:
        return json.loads(resposta["message"]["content"])
    except:
        return {"tipo": "Outros", "urgencia": "MEDIA", "erro": "falha no parse"}

# ─── Executar classificação ──────────────────────────────────────
print("=== CLASSIFICADOR AUTOMÁTICO DE BOs ===")
print()

for i, bo in enumerate(BOS_TESTE, 1):
    print(f"BO #{i}: {bo[:60]}...")
    resultado = classificar_bo(bo)
    print(f"  Tipo:      {resultado.get('tipo')}")
    print(f"  Artigo:    {resultado.get('artigo_cp')}")
    print(f"  Urgência:  {resultado.get('urgencia')}")
    print(f"  Flagrante: {resultado.get('flagrante')}")
    print(f"  Resumo:    {resultado.get('resumo')}")
    print()
