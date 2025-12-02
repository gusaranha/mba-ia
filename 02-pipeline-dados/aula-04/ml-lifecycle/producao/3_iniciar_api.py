"""
3. API DE PRODUÇÃO

API FastAPI que usa o modelo promovido.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import json
import pandas as pd
from pathlib import Path
from typing import Literal

app = FastAPI(title="API de Detecção de Fraudes", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar modelo e metadata
MODEL_PATH = Path("models/producao.pkl")
METADATA_PATH = Path("metadata.json")

if not MODEL_PATH.exists():
    print("❌ Erro: Modelo não encontrado. Execute '2_promover_modelo.py' primeiro.")
    exit(1)

print("🚀 API DE DETECÇÃO DE FRAUDES")
print("=" * 60)
print("\n✅ Carregando modelo de produção...")

with open(MODEL_PATH, "rb") as f:
    modelo = pickle.load(f)

with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

print(f"   Versão: {metadata['versao']}")
print(f"   F1 Score: {metadata['f1_score']:.3f}")
print(f"   Deploy: {metadata['data_deploy']}")
print(f"\n✅ Modelo carregado com sucesso!")


# Schemas
class TransacaoInput(BaseModel):
    valor: float = Field(..., gt=0, description="Valor da transação em R$")
    hora: int = Field(..., ge=0, le=23, description="Hora da transação (0-23)")
    categoria: Literal[
        "alimentacao", "farmacia", "transporte", "vestuario", "restaurante",
        "lazer", "eletronicos", "livros", "assinatura", "supermercado",
        "joias", "viagem", "pix", "transferencia"
    ]
    qtd_transacoes_24h: int = Field(..., ge=0, description="Transações nas últimas 24h")


class PredicaoOutput(BaseModel):
    fraude: bool
    probabilidade: float
    modelo: dict


# Endpoints
@app.get("/")
def root():
    return {
        "servico": "API de Detecção de Fraudes",
        "versao": metadata["versao"],
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "modelo": metadata
    }


@app.post("/predict", response_model=PredicaoOutput)
def predict(transacao: TransacaoInput):
    """Analisa uma transação e retorna se é fraude"""
    try:
        # Mapear categoria para código
        categoria_map = {
            "alimentacao": 1, "farmacia": 2, "transporte": 3,
            "vestuario": 4, "restaurante": 5, "lazer": 6,
            "eletronicos": 7, "livros": 8, "assinatura": 9,
            "supermercado": 10, "joias": 11, "viagem": 12,
            "pix": 13, "transferencia": 14
        }
        
        # Preparar dados
        dados = pd.DataFrame([{
            "valor": transacao.valor,
            "hora": transacao.hora,
            "categoria_cod": categoria_map[transacao.categoria],
            "qtd_transacoes_24h": transacao.qtd_transacoes_24h
        }])
        
        # Predição
        predicao = modelo.predict(dados)[0]
        probabilidade = modelo.predict_proba(dados)[0]
        
        return PredicaoOutput(
            fraude=bool(predicao == 1),
            probabilidade=float(probabilidade[1]),
            modelo={
                "versao": metadata["versao"],
                "f1_score": metadata["f1_score"],
                "deploy_date": metadata["data_deploy"]
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("\nINFO:     Uvicorn running on http://localhost:8000")
    print("INFO:     Docs: http://localhost:8000/docs\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
