#!/bin/bash

# Script para inicializar histórico Git nos exemplos
# Execute após baixar o material da aula

echo "========================================="
echo "   Inicializando Histórico Git"
echo "========================================="
echo ""

# Exemplo Inicial - Versão Estável
echo "📂 Configurando exemplo-inicial..."
cd exemplo-inicial

# Inicializar repositório
git init -b main > /dev/null 2>&1
git config user.email "instrutor@aula4.com"
git config user.name "Instrutor Aula4"

# Criar histórico com 2 commits
git add main.py
git commit -m "feat: Health check" --date="2024-11-01T10:00:00" > /dev/null 2>&1

# Criar commit da versão estável
git commit --allow-empty -m "feat: Versão 1.0 estável" --date="2024-11-10T14:00:00" > /dev/null 2>&1

echo "✅ Histórico criado com sucesso!"
echo ""

# Voltar para diretório raiz
cd ..

# Exemplo Rollback - Versão com Bug
echo "📂 Configurando exemplo-rollback..."
cd exemplo-rollback

# Inicializar repositório
git init -b main > /dev/null 2>&1
git config user.email "instrutor@aula4.com"
git config user.name "Instrutor Aula4"

# Criar commit base (sem bug)
cat > main_temp.py << 'EOF'
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI(title="API Anti-Fraude", version="1.0.0")

class Transacao(BaseModel):
    valor: float = Field(..., gt=0)
    hora_do_dia: int = Field(..., ge=0, le=23)
    distancia_ultima_compra_km: float = Field(..., ge=0)
    numero_transacoes_hoje: int = Field(..., ge=0)
    idade_conta_dias: int = Field(..., ge=0)

class RespostaFraude(BaseModel):
    fraude: bool
    confianca: float
    valor_processado: float
    motivo: str

@app.get("/")
async def root() -> Dict[str, str]:
    return {"mensagem": "API Anti-Fraude v1.0 - Operacional"}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}

@app.post("/analisar", response_model=RespostaFraude)
async def analisar_transacao(transacao: Transacao) -> RespostaFraude:
    valor_processado = float(transacao.valor)
    
    if valor_processado > 10000:
        return RespostaFraude(
            fraude=True,
            confianca=0.95,
            valor_processado=valor_processado,
            motivo="Valor acima do threshold de R$ 10.000"
        )
    
    return RespostaFraude(
        fraude=False,
        confianca=0.90,
        valor_processado=valor_processado,
        motivo="Transação dentro dos padrões normais"
    )
EOF

mv main_temp.py main_stable.py
git add main_stable.py
git commit -m "feat: Versão 1.0 estável" --date="2024-11-10T14:00:00" > /dev/null 2>&1

# Adicionar versão com bug
git add main.py
git commit -m "feat: Adicionar normalização (v1.1)" --date="2024-11-13T14:00:00" > /dev/null 2>&1

echo "✅ Histórico criado com sucesso!"
echo ""

cd ..

echo "========================================="
echo "✅ Setup completo!"
echo "========================================="
echo ""
echo "Próximos passos:"
echo "  1. cd exemplo-inicial"
echo "  2. git log --oneline"
echo "  3. Explore o histórico!"
echo ""
