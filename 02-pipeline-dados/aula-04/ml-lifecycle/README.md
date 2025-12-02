# 🎬 Demo: Ciclo de Vida ML Completo

Demonstração prática do ciclo de vida de um modelo de Machine Learning em produção.

Maria trabalha no setor de fraudes de um banco. É **30 de Outubro de 2025**.  
Ela tem dados históricos e precisa criar um sistema para detectar fraudes automaticamente.

Vamos acompanhar a jornada completa:
1. **Experimentos** - Qual modelo usar?
2. **Deploy** - Colocar em produção
3. **Consumo** - Sistema funcionando
4. **Monitoramento** - Detectar degradação
5. **Retreinamento** - Atualizar o modelo

## 🚀 Quick Start

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Seguir o roteiro
Abra `ROTEIRO_APRESENTACAO.md` e execute os scripts na ordem.

## 📁 Estrutura

```
ml-lifecycle-demo/
├── dados/                         # Dados de Outubro e Novembro 2025
│   ├── outubro_2025.csv          # ✅ 2000 transações, 10% fraude
│   ├── novembro_2025.csv         # ✅ 2000 transações, 15% fraude (drift!)
│   ├── gerar_outubro.py
│   ├── gerar_novembro.py
│   └── README.md
│
├── experimentos/                  # Fase 1: Testar modelos
│   └── 1_rodar_experimentos.py   # Testa 9 modelos, salva no MLflow
│
├── producao/                      # Fase 2 & 3: Deploy e consumo
│   ├── 2_promover_modelo.py      # Promove melhor modelo
│   ├── 3_iniciar_api.py          # API FastAPI
│   └── models/
│       └── producao.pkl          # (gerado automaticamente)
│
├── monitoramento/                 # Fase 4: Detectar degradação
│   └── 4_avaliar_performance.py  # Compara Out vs Nov
│
├── retreinamento/                 # Fase 5: Atualizar modelo
│   ├── 5_retreinar_modelo.py     # Combina Out+Nov, retreina
│   └── 6_promover_v2.py          # Promove v2.0
│
├── frontend/                      # UI para testar
│   └── index.html
│
├── mlruns/                        # (gerado pelo MLflow)
├── requirements.txt
└── ROTEIRO_APRESENTACAO.md       # 👈 COMECE AQUI!
```

## 🎯 Sequência de Execução

### Fase 1: Experimentos
```bash
cd experimentos
python 1_rodar_experimentos.py
mlflow ui --host 127.0.0.1 --port 5000 # Visualizar em http://localhost:5000
```

### Fase 2: Deploy
```bash
cd ../producao
python 2_promover_modelo.py
python 3_iniciar_api.py  # API em http://localhost:8000
```

### Fase 3: Consumo
```
Abrir frontend/index.html no navegador
```

### Fase 4: Monitoramento
```bash
cd ../monitoramento
python 4_avaliar_performance.py
```

### Fase 5: Retreinamento
```bash
cd ../retreinamento
python 5_retreinar_modelo.py
python 6_promover_v2.py

# Reiniciar API
cd ../producao
python 3_iniciar_api.py
```

## 📊 O que você vai ver

### Outubro (v1.0)
- 9 modelos testados
- Melhor: XGBoost com F1 ~95%
- Sistema em produção funcionando

### Novembro (degradação)
- Taxa de fraude aumentou: 10% → 15%
- Novos padrões: PIX, Transferência
- Fraudes em horário comercial
- Performance caiu: F1 ~95% → ~82%

### Retreinamento (v2.0)
- Dados Out+Nov combinados (4000 registros)
- Novo modelo: F1 ~97%
- Performance recuperada!

## 🎓 Conceitos Demonstrados

- ✅ **Experiment Tracking** (MLflow)
- ✅ **Model Versioning**
- ✅ **Concept Drift Detection**
- ✅ **Model Monitoring**
- ✅ **Automated Retraining**
- ✅ **Production Deployment**
- ✅ **API Development** (FastAPI)


