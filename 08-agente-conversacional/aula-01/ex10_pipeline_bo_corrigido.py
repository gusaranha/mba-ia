# ex10_pipeline_bo_corrigido.py
# Ex.10 Pipeline completo: BO -> Análise -> Relatório
#
# ATENÇÃO: o conteúdo deste exercício está incompleto/truncado no arquivo
# de origem (src/aula01/aula01.txt) — a etapa2_extrair() termina no meio da
# chamada a debug_print(), faltando o parse do JSON, as etapas 3 e 4
# (mencionadas nos comentários "[2/4]", "[1/4]") e o bloco de execução
# principal do pipeline. O código abaixo reproduz fielmente apenas o que
# existe na fonte.
#
# Dependências:
#   pip install ollama
# (json e time são bibliotecas padrão do Python, não precisam ser instaladas)
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama
import json
import time

# ─── BO de entrada ──────────────────────────────────────────────
BO_ENTRADA = """
BOLETIM DE OCORRÊNCIA Nº 2025/007890
Data: 20/03/2025  Hora: 09h15  Delegacia: 5ª DP - Vila Nova

Vítima: Ana Paula Rodrigues, 28 anos, balconista
RG: 45.678.901-2  CPF: 123.456.789-00
Tel: (11) 99876-5432

Relato: A declarante informa que recebeu ligação de suposto funcionário
do banco informando que sua conta havia sido bloqueada. O indivíduo
solicitou que ela instalasse um aplicativo no celular e fornecesse
seus dados bancários para desbloqueio. Após seguir as instruções,
percebeu que R$ 4.200,00 foram transferidos de sua conta sem autorização.

Suspeitos: Não identificados. Ligação feita de número não cadastrado.
"""

def debug_print(titulo: str, conteudo: str) -> None:
    """Mostra a resposta crua do modelo para facilitar diagnóstico."""
    print(f"\n--- DEBUG: {titulo} ---")
    print(conteudo)
    print("--- FIM DEBUG ---\n")

# ─── Etapa 1: Classificar o crime ───────────────────────────────
def etapa1_classificar(bo_texto: str) -> dict:
    """
    Etapa 1: identifica o tipo de crime do BO.
    CORREÇÃO: prompt explícito com formato exato esperado,
    evitando que o modelo use nomes de chave diferentes.
    """
    print("  [1/4] Classificando crime...")

    prompt = f"""Você é um especialista em tipificação penal da Polícia Civil.
Analise o boletim de ocorrência abaixo e classifique o crime.

Boletim de Ocorrência:
{bo_texto}

Retorne APENAS um JSON válido EXATAMENTE neste formato, sem nenhum texto adicional:
{{
  "tipo": "nome do crime (ex: estelionato, furto, roubo)",
  "artigo_cp": "artigo do Código Penal aplicável, no formato Art. XXX",
  "urgencia": "ALTA ou MEDIA ou BAIXA"
}}"""

    resposta = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        format="json", options={"temperature": 0}
    )

    bruto = resposta["message"]["content"]
    debug_print("Etapa 1 - Classificação", bruto)

    dados = json.loads(bruto)

    # ── Normalização: aceita variações de nome de chave que o modelo
    #    às vezes usa, garantindo que sempre teremos "tipo" preenchido ──
    if not dados.get("tipo"):
        for chave_alternativa in ["tipo_crime", "classificacao", "crime", "tipificacao"]:
            if dados.get(chave_alternativa):
                dados["tipo"] = dados[chave_alternativa]
                break

    return dados

# ─── Etapa 2: Extrair dados estruturados ────────────────────────
def etapa2_extrair(bo_texto: str) -> dict:
    """Etapa 2: extrai dados estruturados do BO."""
    print("  [2/4] Extraindo dados estruturados...")

    prompt = f"""Extraia as informações do boletim de ocorrência abaixo.

Boletim de Ocorrência:
{bo_texto}

Retorne APENAS um JSON válido EXATAMENTE neste formato, sem texto adicional:
{{
  "vitima": "nome da vítima",
  "crime": "resumo curto do que aconteceu",
  "prejuizo": "valor do prejuízo financeiro, se houver (ex: R$ 4.200,00)",
  "suspeitos": "descrição dos suspeitos ou 'não identificados'",
  "modo_operandi": "breve descrição de como o crime foi cometido"
}}"""

    resposta = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        format="json", options={"temperature": 0}
    )

    bruto = resposta["message"]["content"]
    debug_print("Etapa 2 - Extração", bruto)

    # [TRUNCADO NA FONTE] — a partir daqui o arquivo original é cortado:
    # falta o json.loads(bruto) desta etapa, as etapas 3/4 do pipeline
    # (ex.: análise de urgência e geração de relatório final) e o bloco
    # de execução principal que orquestra etapa1_classificar() e
    # etapa2_extrair().
