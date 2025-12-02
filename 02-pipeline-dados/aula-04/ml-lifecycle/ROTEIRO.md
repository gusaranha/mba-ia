### 1. Instalar dependências
```bash
cd ml-lifecycle-demo
pip install -r requirements.txt
```


### 2. Verificar estrutura
```
ml-lifecycle-demo/
├── dados/
│   ├── outubro_2025.csv          ✅ 2000 transações, 10% fraude
│   ├── novembro_2025.csv         ✅ 2000 transações, 15% fraude
│   └── README.md
├── experimentos/
│   └── 1_rodar_experimentos.py
├── producao/
│   ├── 2_promover_modelo.py
│   └── 3_iniciar_api.py
├── monitoramento/
│   └── 4_avaliar_performance.py
├── retreinamento/
│   ├── 5_retreinar_modelo.py
│   └── 6_promover_v2.py
└── frontend/
    └── index.html
```



**DADOS:**
```bash
cd ml-lifecycle-demo

outubro_2025.csv    <- Dados históricos (treino)
novembro_2025.csv   <- Dados futuros (produção)
```



## 1️⃣ EXPERIMENTOS 


Maria testa 9 modelos diferentes para encontrar o melhor.

### EXECUTAR:
```bash
cd experimentos
python 1_rodar_experimentos.py
```

### O QUE APARECE:
```
🔬 RODANDO EXPERIMENTOS - Outubro 2025
════════════════════════════════════════════════════════════

Dataset: 2000 transações
Fraudes: 200 (10%)

Testando configurações...

✅ RandomForest (n=100, depth=10)        | F1: 0.940
✅ RandomForest (n=200, depth=15)        | F1: 0.945
✅ RandomForest (n=500, depth=20)        | F1: 0.942

✅ XGBoost (n=100, lr=0.1)               | F1: 0.958 ⭐
✅ XGBoost (n=200, lr=0.05)              | F1: 0.955
✅ XGBoost (n=300, lr=0.1)               | F1: 0.952

✅ GradientBoosting (n=100, lr=0.1)      | F1: 0.948
✅ GradientBoosting (n=200, lr=0.05)     | F1: 0.951
✅ GradientBoosting (n=300, lr=0.1)      | F1: 0.946

✅ LogisticRegression (C=1.0)            | F1: 0.885
✅ LogisticRegression (C=0.1)            | F1: 0.878
✅ LogisticRegression (C=10.0)           | F1: 0.890

════════════════════════════════════════════════════════════
🏆 VENCEDOR: XGBoost (n=100, lr=0.1)
   F1 Score: 0.958
   Run ID: a1b2c3d4e5f6

💾 Todos experimentos salvos no MLflow

👉 Execute 'mlflow ui' para visualizar
```

### MLflow UI:
```
mlflow ui &
```

**Navegador:** http://localhost:5000

- Lista de 9 runs
- Clica na coluna F1 para ordenar
- XGBoost aparece no topo
- Clica no run



## 2️⃣ DEPLOY 
```
cd ../producao
python 2_promover_modelo.py
```

### O QUE APARECE:
```
📦 PROMOVENDO MODELO PARA PRODUÇÃO
════════════════════════════════════════════════════════════

✅ Melhor modelo identificado:
   Algoritmo: XGBoost (n=100, lr=0.1)
   F1 Score: 0.958
   Precision: 0.952
   Recall: 0.964
   Run ID: a1b2c3d4e5f6

📥 Carregando modelo do MLflow...
✅ Modelo salvo em: models/producao.pkl

✅ Metadata atualizada:
{
  "versao": "v1.0",
  "data_deploy": "2025-10-30",
  "data_treino": "outubro_2025",
  "algoritmo": "XGBoost (n=100, lr=0.1)",
  "f1_score": 0.958,
  "precision": 0.952,
  "recall": 0.964,
  "run_id": "a1b2c3d4e5f6",
  "n_transacoes_treino": 2000,
  "taxa_fraude_treino": 0.10
}

🚀 Modelo v1.0 pronto para produção!
```

### INICIA A API:
```bash
python 3_iniciar_api.py
```

### O QUE APARECE:
```
🚀 API DE DETECÇÃO DE FRAUDES
════════════════════════════════════════════════════════════

✅ Carregando modelo de produção...
   Versão: v1.0
   F1 Score: 0.958
   Deploy: 2025-10-30

✅ Modelo carregado com sucesso!

INFO:     Uvicorn running on http://localhost:8000
INFO:     Docs: http://localhost:8000/docs
```


## 3️⃣ CONSUMO (5min)

###  FRONTEND:
```bash
open ../frontend/index.html
# Ou simplesmente abre no navegador
```

### PREENCHER (transação suspeita):
- Valor: 8500
- Hora: 2
- Categoria: Eletrônicos
- Transações 24h: 18

### CLICAR: "Analisar"

### RESULTADO:
```
🚨 FRAUDE DETECTADA

Probabilidade: 94.3%
████████████████████░

Modelo: v1.0 | F1: 95.8% | Deploy: 2025-10-30
```

### TESTAR (transação legítima):
- Valor: 45
- Hora: 14
- Categoria: Alimentação
- Transações 24h: 2

### RESULTADO:
```
✅ Transação Aprovada

Probabilidade: 3.2%
███░░░░░░░░░░░░░░░░░

Modelo: v1.0 | F1: 95.8% | Deploy: 2025-10-30
```


## 4️⃣ MONITORAMENTO 


### EXECUTAR:
```bash
cd ../monitoramento
python 4_avaliar_performance.py
```

### O QUE APARECE:
```
📊 RELATÓRIO DE MONITORAMENTO - Novembro 2025
════════════════════════════════════════════════════════════

📅 Período de Análise
   Treino: Outubro 2025 (2000 transações, 10% fraude)
   Produção: Novembro 2025 (2000 transações, 15% fraude)

🤖 Modelo em Produção
   Versão: v1.0
   Deploy: 2025-10-30
   Algoritmo: XGBoost (n=100, lr=0.1)

📈 MÉTRICAS - OUTUBRO (Baseline)
   F1 Score:  0.958  ━━━━━━━━━━━━━━━━━━━━ 100%
   Precision: 0.952  ━━━━━━━━━━━━━━━━━━━━  99%
   Recall:    0.964  ━━━━━━━━━━━━━━━━━━━━ 101%

📉 MÉTRICAS - NOVEMBRO (Produção)
   F1 Score:  0.824  ━━━━━━━━━━━━━░░░░░░░  86%  ⚠️  -14.0%
   Precision: 0.792  ━━━━━━━━━━━░░░░░░░░░  83%  ⚠️  -16.8%
   Recall:    0.860  ━━━━━━━━━━━━━░░░░░░░  89%  ⚠️  -10.8%

🚨 ALERTAS DETECTADOS

  1. DEGRADAÇÃO CRÍTICA
     F1 Score caiu 14.0 pontos percentuais
     Limite: 10% | Atual: 14.0%
     Status: ⛔ CRÍTICO

  2. MUDANÇA NO PADRÃO DE FRAUDES
     Taxa Outubro: 10%
     Taxa Novembro: 15% (+50%)
     
  3. NOVOS PADRÕES IDENTIFICADOS
     • Valores médios de fraude: R$ 3415 → R$ 4352 (+27%)
     • Novas categorias detectadas: pix, transferencia
     • Horário médio fraudes: 8h → 12h

💡 RECOMENDAÇÃO: RETREINAMENTO URGENTE

   Ações sugeridas:
   1. Retreinar com dados Outubro + Novembro
   2. Ajustar para nova taxa de fraude (15%)
   3. Incorporar novos padrões
   4. Promover novo modelo para produção

════════════════════════════════════════════════════════════
👉 Próximo passo: Execute '../retreinamento/5_retreinar_modelo.py'
```


## 5️⃣ RETREINAMENTO 

```bash
cd ../retreinamento
python 5_retreinar_modelo.py
```

### O QUE APARECE:
```
🔄 RETREINAMENTO DO MODELO
════════════════════════════════════════════════════════════

📊 Combinando dados...
   Outubro 2025:  2000 transações (10% fraude)
   Novembro 2025: 2000 transações (15% fraude)
   ──────────────────────────────────────────────────────────
   Total:         4000 transações (12.5% fraude)

🔬 Rodando experimentos...

✅ RandomForest (n=100, depth=10)        | F1: 0.935
✅ RandomForest (n=200, depth=15)        | F1: 0.941
✅ RandomForest (n=500, depth=20)        | F1: 0.938

✅ XGBoost (n=100, lr=0.1)               | F1: 0.976 ⭐
✅ XGBoost (n=200, lr=0.05)              | F1: 0.972
✅ XGBoost (n=300, lr=0.1)               | F1: 0.969

✅ GradientBoosting (n=100, lr=0.1)      | F1: 0.948
✅ GradientBoosting (n=200, lr=0.05)     | F1: 0.953
✅ GradientBoosting (n=300, lr=0.1)      | F1: 0.946

✅ LogisticRegression (C=1.0)            | F1: 0.892
✅ LogisticRegression (C=0.1)            | F1: 0.885
✅ LogisticRegression (C=10.0)           | F1: 0.897

════════════════════════════════════════════════════════════
🏆 NOVO VENCEDOR: XGBoost (n=100, lr=0.1)
   F1 Score (treino): 0.976  (+1.8% vs v1.0)
   Run ID: x9y8z7w6v5

✅ Validação em dados de Novembro:
   F1 Score: 0.971  (+14.7% vs v1.0 degradado)
   
💾 Experimentos salvos no MLflow

👉 Próximo passo: Execute '6_promover_v2.py'
```

### PROMOVER v2.0:
```bash
python 6_promover_v2.py
```

### O QUE APARECE:
```
📦 PROMOVENDO MODELO v2.0
════════════════════════════════════════════════════════════

✅ Novo modelo identificado:
   Algoritmo: XGBoost (n=100, lr=0.1)
   F1 Score (treino): 0.976
   Run ID: x9y8z7w6v5

📊 COMPARAÇÃO v1.0 vs v2.0

                      v1.0      v2.0    Melhoria
   ──────────────────────────────────────────────
   F1 (treino)        0.958     0.976    +1.8%
   Dados              2000      4000     +100%
   Taxa fraude        10%       12.5%    Ajustado

✅ Modelo salvo em: ../producao/models/producao.pkl

✅ Metadata atualizada:
{
  "versao": "v2.0",
  "data_deploy": "2025-11-30",
  "data_treino": "outubro_novembro_2025",
  "algoritmo": "XGBoost (n=100, lr=0.1)",
  "f1_score": 0.976,
  "precision": 0.974,
  "recall": 0.978,
  "run_id": "x9y8z7w6v5",
  "n_transacoes_treino": 4000,
  "taxa_fraude_treino": 0.125,
  "changelog": [
    "Retreinado com dados Out+Nov (4000 registros)",
    "Taxa de fraude ajustada: 12.5%",
    "Novos padrões incorporados",
    "Performance: +1.8% vs v1.0"
  ]
}

🚀 Modelo v2.0 pronto para deploy!

👉 Reinicie a API: 'python ../producao/3_iniciar_api.py'
```

### REINICIAR A API:
```bash
# Ctrl+C na API antiga
cd ../producao
python 3_iniciar_api.py
```

### O QUE APARECE:
```
🚀 API DE DETECÇÃO DE FRAUDES
════════════════════════════════════════════════════════════

✅ Carregando modelo de produção...
   Versão: v2.0  🆕
   F1 Score: 0.976
   Deploy: 2025-11-30

✅ Modelo carregado com sucesso!

INFO:     Uvicorn running on http://localhost:8000
```

### FRONTEND:
- Mesma transação suspeita de antes
- Agora mostra: "Modelo v2.0 | F1: 97.6% | Deploy: 2025-11-30"


