# Aula 1: Ciclo de Vida de um Modelo de Machine Learning

## Descrição

Processo completo de desenvolvimento de um modelo de Machine Learning, desde a definição do problema até o monitoramento em produção. Caso de uso: análise de transações financeiras para demonstrar as 8 etapas.

## Estrutura do Projeto

```
aula_1/
├── data/                          # Datasets
│   ├── transacoes.csv            # Dataset limpo (500k linhas)
│   ├── transacoes_sujas.csv      # Dataset com problemas
│   ├── transacoes_janeiro.csv    # Dados mensais para
│   ├── transacoes_fevereiro.csv  # demonstração de
│   ├── transacoes_marco.csv      # concept drift
│   ├── transacoes_abril.csv      # (degradação de
│   ├── transacoes_maio.csv       # performance ao
│   └── transacoes_junho.csv      # longo do tempo)
│
├── demos/                         # Scripts de demonstração
│   ├── demo_1_carregar_dados.py
│   ├── demo_2_exploracao.py
│   ├── demo_3_visualizacao.py
│   ├── demo_4_dados_sujos.py
│   ├── demo_5_limpar_dados.py
│   ├── demo_6_treinar_modelo.py
│   ├── demo_7_validacao.py
│   ├── demo_8_notebook_caotico.ipynb
│   ├── demo_9_script_producao.py
│   └── demo_10_concept_drift.py
│
├── exercicios/                    # Exercícios para prática
│   ├── exercicio_1_exploracao.py
│   ├── exercicio_2_filtros.py
│   └── exercicio_3_limpeza.py
│
├── models/                        # Modelos treinados (gerado automaticamente)
│   ├── modelo_fraude.pkl
│   ├── label_encoder.pkl
│   └── metricas.txt
│
├── requirements.txt              # Dependências Python
├── gerar_datasets.py             # Script para gerar todos os CSVs
└── README.md                     # Este arquivo
```

## Instalação

### 1. Criar ambiente virtual (recomendado)

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```



## Como Usar

### Demonstrações

Execute os scripts na ordem numérica para acompanhar a progressão da aula:

```bash
cd demos

# Etapas 1-2: Problema e Coleta
python demo_1_carregar_dados.py

# Etapa 3: Exploração
python demo_2_exploracao.py
python demo_3_visualizacao.py

# Etapa 4: Limpeza
python demo_4_dados_sujos.py
python demo_5_limpar_dados.py

# Etapa 5: Treinamento
python demo_6_treinar_modelo.py

# Etapa 6: Validação
python demo_7_validacao.py

# Etapa 7: Produção
jupyter notebook demo_8_notebook_caotico.ipynb  # Ver más práticas
python demo_9_script_producao.py                 # Ver boas práticas

# Etapa 8: Monitoramento
python demo_10_concept_drift.py
```

### Exercícios

Abra os arquivos em `exercicios/` e complete os TODOs marcados:

```bash
cd exercicios

# Exercício 1: Comandos básicos
python exercicio_1_exploracao.py

# Exercício 2: Filtros e agregações
python exercicio_2_filtros.py

# Exercício 3: Limpeza de dados
python exercicio_3_limpeza.py
```

## As 8 Etapas do Ciclo de Vida de ML

1. **🎯 Definir Problema:** Entender o problema de negócio e traduzir para ML
2. **📊 Coletar Dados:** Identificar fontes e extrair dados relevantes
3. **🔍 Explorar Dados:** Conhecer características, distribuições e padrões
4. **🧹 Limpar Dados:** Remover/corrigir problemas (nulos, duplicatas, outliers)
5. **🧪 Treinar Modelo:** Escolher algoritmo e treinar com dados históricos
6. **✅ Validar Modelo:** Avaliar performance com dados não vistos
7. **🚀 Produção:** Estruturar código para ambiente operacional
8. **📈 Monitorar:** Acompanhar performance e retreinar quando necessário

## Conceitos Importantes

### Dados Tabulares
- Estrutura de tabela (linhas e colunas)
- Cada linha = 1 registro (ex: 1 transação)
- Cada coluna = 1 característica (ex: valor, hora)
- Formato mais comum em empresas

### Features vs Target
- **Features (X):** Características usadas para prever (valor, hora, categoria)
- **Target (y):** O que queremos prever (is_fraud)

### Train-Test Split
- Dividir dados em treino (70%) e teste (30%)
- Treino: modelo aprende
- Teste: modelo é avaliado (nunca viu antes!)
- Evita overfitting (decorar vs aprender)

### Métricas
- **Acurácia:** % de acertos totais (pode enganar com classes desbalanceadas)
- **Precisão:** Das previstas como fraude, quantas eram realmente?
- **Recall:** Das fraudes reais, quantas o modelo detectou?
- **F1-Score:** Média harmônica de precisão e recall (melhor para desbalanceamento)

### Notebook vs Script
- **Notebook (.ipynb):** Ideal para exploração, experimentação, visualizações
- **Script (.py):** Ideal para produção, automação, reprodutibilidade
- Ambos são importantes e complementares!

### Concept Drift
- Degradação de performance ao longo do tempo
- Causa: dados/padrões mudam, mas modelo não
- Solução: monitoramento + retreinamento periódico

## Dados

### Dataset Principal (`transacoes.csv`)
- **Linhas:** 500.000 transações
- **Colunas:**
  - `id`: Identificador único (int)
  - `valor`: Montante em reais (float)
  - `categoria`: Tipo de produto {A, B, C, D}
  - `hora`: Hora do dia {0-23}
  - `is_fraud`: Rótulo {0=legítima, 1=fraude}
- **Proporção:** 95% legítimas, 5% fraudes

### Dataset Sujo (`transacoes_sujas.csv`)
Mesma estrutura, mas com problemas intencionais:
- 342 valores nulos em `valor`
- 89 valores nulos em `categoria`
- 156 linhas duplicadas
- 23 valores negativos
- 67 categorias inválidas {X, Y, Z}

### Datasets Mensais
Arquivos de janeiro a junho para demonstrar concept drift.

## Observações


- O diretório `models/` é criado automaticamente pelos scripts de treinamento