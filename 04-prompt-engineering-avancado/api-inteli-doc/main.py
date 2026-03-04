from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

app = FastAPI(title="IntelliDoc PCDF - Módulo 1")

# 1. Conexão com a Memória (Igual ao script anterior)
chroma_client = chromadb.PersistentClient(path="./banco_vetorial")
ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="nomic-embed-text"
)
collection = chroma_client.get_collection(name="laudos", embedding_function=ollama_ef)

# 2. Conexão com o Cérebro (Llama)
client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')


class BoletimOcorrencia(BaseModel):
    relato: str
    unidade: str = "PCDF - IC"


class Pergunta(BaseModel):
    texto: str


@app.get("/")
def verificar_status():
    return {"status": "online"}


@app.post("/analisar_inteligente")
def analisar_com_ia(bo: BoletimOcorrencia):
    # Ensinamos o padrão através de exemplos.
    prompt_sistema = """
    Você é um experiente perito laboratorial 
    
    REGRAS OBRIGATÓRIAS:
    1. Analise o relato.
    2. Classifique ESTRITAMENTE em uma destas categorias: [NENHUM, BAIXA, MEDIA, ALTA].
    3. Responda APENAS a palavra da categoria. Sem ponto final.
    
    EXEMPLOS DE TREINAMENTO (Siga este padrão):
    
    Relato: "A análise laboratorial verificou que o líquido era de fato a substância correta."
    Classificação: severidade: NENHUMA
    
    Relato: "O frasco da bebida estava sem nenhum rótulo com informações sobre a bebida"
    Classificação: severidade: BAIXA
    
    Relato: "A análise laboratorial verificou que o líquido estava misturado com água."
    Classificação: severidade: MEDIA
    
    Relato: "A análise laboratorial verificou que o líquido estava misturado com outras substâncias."
    Classificação: severidade: ALTA
    
    Agora classifique o novo relato:
    """

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": bo.relato}
        ],
        temperature=0.0  # Temperatura ZERO para máxima precisão
    )

    return {
        "tecnica": "Few-Shot Prompting",
        "classificacao_ia": response.choices[0].message.content
    }


@app.post("/analisar_cot")
def analisar_raciocinio(bo: BoletimOcorrencia):
    print(f"Raciocínando sobre: {bo.relato}...")

    # PROMPT CoT: Passo a Passo
    prompt_cot = """
    Aja como um Delegado que analisa um laudo pericial. Siga este roteiro mental:

    PASSO 1: Fatos - Liste o que realmente aconteceu.
    PASSO 2: Adulteração - A bebida examinada foi adulterada? (Sim/Não)
    PASSO 3: Severidade - As substâncias identificadas podem ocasionar danos à saúde humana?

    Com base nisso, defina a tipificação penal.

    Formato de Resposta:
    RACIOCINIO: [Sua análise detalhada]
    VEREDITO SOBRE A ADULTERAÇÃO DA BEBIDA: [SIM ou NÃO]
    VEREDITO SOBRE A TOXIDADE DAS SUBSTÂNCIAS: [NENHUM, BAIXO, MEDIO, ALTO]
    """

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": prompt_cot},
            {"role": "user", "content": bo.relato}
        ],
        temperature=0.1  # Leve criatividade para escrever a explicação
    )

    return {
        "tecnica": "Chain of Thought (CoT)",
        "analise_completa": response.choices[0].message.content
    }


@app.post("/perguntar")
def investigar_caso(pergunta: Pergunta):
    print(f"Buscando evidências para: {pergunta.texto}")

    # PASSO 1: Retrieval (Recuperação)
    # Buscamos no banco os 3 trechos mais parecidos com a pergunta
    resultados = collection.query(
        query_texts=[pergunta.texto],
        n_results=3  # Traz os top 3 pedaços mais relevantes
    )

    # Juntamos os pedaços recuperados em um único texto
    contexto_recuperado = "\n".join(resultados['documents'][0])
    print(f"Contexto encontrado: {contexto_recuperado}")

    # PASSO 2: Augmented Generation (Geração Aumentada)
    # Colamos o contexto no prompt do sistema
    prompt_sistema = f"""
    Você é um assistente de inteligência policial.
    Responda à pergunta do usuário usando APENAS o contexto abaixo.
    Se a resposta não estiver no contexto, diga "Não consta nos autos".

    CONTEXTO DOS AUTOS:
    {contexto_recuperado}
    """

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": pergunta.texto}
        ],
        temperature=0.0
    )

    return {
        "pergunta": pergunta.texto,
        "resposta": response.choices[0].message.content,
        "fontes_utilizadas": resultados['documents']
    }
