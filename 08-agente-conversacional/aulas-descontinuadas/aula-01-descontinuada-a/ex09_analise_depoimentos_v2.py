# ex09_analise_depoimentos_v2.py
# Ex.09 Analisador de consistência de depoimentos
#
# ATENÇÃO: o conteúdo deste exercício está incompleto/truncado no arquivo
# de origem (src/aula01/aula01.txt) — o prompt dentro de analisar_contradicoes()
# termina no meio de uma string JSON, faltando o restante do prompt, a
# chamada a ollama.chat(), o parse do JSON e o bloco de execução principal.
# O código abaixo reproduz fielmente apenas o que existe na fonte.
#
# Dependências:
#   pip install ollama
# (json é biblioteca padrão do Python, não precisa instalar)
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama
import json

# ─── Depoimentos fictícios para análise ─────────────────────────
DEPOIMENTO_VITIMA = """
Eu estava na padaria às 13h00 quando dois homens entraram e anunciaram o assalto.
Um deles usava camiseta vermelha e o outro estava de jaqueta preta.
Eles ficaram cerca de 10 minutos no local. Fugiram em um carro branco.
Era um Fiat Uno. Não consegui ver as placas.
"""

DEPOIMENTO_TESTEMUNHA = """
Vi dois rapazes saindo correndo da padaria por volta de 13h45.
Um usava blusa azul e o outro de blusão escuro.
Entraram num veículo de cor prata — me pareceu um Gol.
O ocorrido durou uns 5 minutos no máximo.
"""

def debug_print(titulo: str, conteudo: str) -> None:
    """Mostra a resposta crua do modelo para facilitar diagnóstico."""
    print(f"\n{'=' * 60}")
    print(f"DEBUG — {titulo}")
    print('=' * 60)
    print(conteudo)
    print('=' * 60 + "\n")

def normalizar_lista(dados: dict, chave_principal: str, alternativas: list) -> list:
    """
    Garante que sempre retornamos uma lista, mesmo que o modelo
    tenha usado um nome de chave diferente do esperado.
    """
    if dados.get(chave_principal):
        valor = dados[chave_principal]
        return valor if isinstance(valor, list) else [valor]

    for alt in alternativas:
        if dados.get(alt):
            valor = dados[alt]
            return valor if isinstance(valor, list) else [valor]

    return []

def analisar_contradicoes(dep1: str, dep2: str,
                           nome1: str = "Vítima",
                           nome2: str = "Testemunha") -> dict:
    """
    Compara dois depoimentos e identifica divergências.
    Útil em investigações para apontar inconsistências.

    Retorna dicionário com:
        contradicoes:     lista de contradições encontradas
        elementos_comuns: pontos em que concordam
        credibilidade:    avaliação geral de credibilidade
        recomendacao:     próximas diligências sugeridas
        resumo_analise:   parágrafo com a análise geral
    """
    prompt = f"""Você é um investigador experiente da Polícia Civil.
Compare os dois depoimentos abaixo, frase por frase, e identifique
TODAS as contradições factuais entre eles.

Depoimento da {nome1}:
{dep1}

Depoimento da(o) {nome2}:
{dep2}

Preste atenção especial a estas três categorias de divergência:
1. HORÁRIO mencionado por cada depoente
2. DESCRIÇÃO das roupas/aparência dos suspeitos
3. VEÍCULO usado na fuga (cor e modelo)

Retorne APENAS um JSON válido EXATAMENTE neste formato, sem texto adicional:
{{
  "contradicoes": [
    "Divergência de horário: vítima diz 13h00, testemunha diz 13h45",
    "Divergência na descrição das roupas: ...",
    "Divergência no veículo: ..."
  ],
"""
    # [TRUNCADO NA FONTE] — o restante do prompt (chaves elementos_comuns,
    # credibilidade, recomendacao, resumo_analise), a chamada a ollama.chat(),
    # o parse do JSON de resposta e o bloco de execução principal não
    # estavam presentes em aula01.txt.
