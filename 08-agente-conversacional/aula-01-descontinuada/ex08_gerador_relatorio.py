# ex08_gerador_relatorio.py
# Ex.08 Gerador de Relatório Policial
#
# Dependências:
#   pip install ollama
# (datetime é biblioteca padrão do Python, não precisa instalar)
# Requer também o servidor Ollama rodando localmente com o modelo "llama3"
# baixado (ollama pull llama3).

import ollama
from datetime import datetime  # para trabalhar com datas

# ─── Dados de entrada (simulando sistema de gestão) ─────────────
DADOS_BO = {
    "numero":       "2025/004521",
    "data":         "15/03/2025",
    "hora":         "14h32",
    "delegacia":    "1ª DP - Centro",
    "natureza":     "Furto qualificado (Art. 155, §4º, I do CP)",
    "vitima":       "João Carlos Pereira, 34 anos",
    "bem":          "iPhone 15 Pro Max",
    "valor":        "R$ 8.500,00",
    "local":        "Rua XV de Novembro, Centro",
    "suspeitos":    "Não identificados",
    "testemunhas":  "Nenhuma localizada",
}

# ─── Função geradora de relatório ───────────────────────────────
def gerar_relatorio(dados: dict, tipo_relatorio: str = "inicial") -> str:
    """
    Gera relatório policial a partir de dados estruturados.

    Parâmetros:
        dados:          dicionário com os dados do BO
        tipo_relatorio: "inicial", "investigacao" ou "conclusao"
    Retorna:
        texto do relatório formatado
    """
    # Converte o dicionário em texto legível para o modelo
    dados_texto = "\n".join([f"  {k}: {v}" for k, v in dados.items()])

    prompt = f"""Você é um escrivão de polícia sênior.
Gere um relatório policial {tipo_relatorio} profissional e formal com base
nos dados abaixo. Use linguagem técnica e jurídica adequada.
Estruture em parágrafos: Dos Fatos, Da Qualificação das Partes,
Das Diligências Iniciais, Das Conclusões Preliminares.

Dados do BO:
{dados_texto}

Data de geração: {datetime.now().strftime("%d/%m/%Y às %H:%M")}
"""

    resposta = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.3,   # leve criatividade para redigir bem
            "num_predict": 800,   # relatório longo
        }
    )
    return resposta["message"]["content"]

# ─── Gerar e exibir o relatório ─────────────────────────────────
print("=== GERANDO RELATÓRIO POLICIAL ===")
relatorio = gerar_relatorio(DADOS_BO, "inicial")
print(relatorio)

# Salvar em arquivo
nome_arquivo = f"relatorio_bo_{DADOS_BO['numero'].replace('/','_')}.txt"
with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write(relatorio)
print(f"\n✅ Relatório salvo em: {nome_arquivo}")
