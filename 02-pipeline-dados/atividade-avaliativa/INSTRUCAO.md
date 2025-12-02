# Trabalho em Grupo: Pipeline de ML Guiado

## Objetivo
Aplicar os conceitos das Aulas 1, 2 e 3 construindo um pipeline de ML funcional com validação de dados e versionamento adequado.

---

## Contexto

Vocês foram contratados como cientistas de dados júnior na empresa "TechBank". O time anterior deixou um projeto incompleto de classificação de clientes para campanha de marketing. O dataset está pronto, a estrutura do projeto existe, mas faltam partes críticas do código.

**Sua missão:** completar o pipeline, garantir que os dados sejam validados, e entregar um repositório organizado com histórico de commits adequado.

---

## Material Fornecido

```
trabalho_grupo/
├── data/
│   └── clientes_campanha.csv      # Dataset (5000 clientes)
├── pipeline/
│   ├── carregar.py                # TODO: completar
│   ├── validar.py                 # TODO: completar  
│   ├── treinar.py                 # TODO: completar
│   └── avaliar.py                 # Pronto
├── main.py                        # Script principal (quase pronto)
├── requirements.txt               # Dependências
└── RESPOSTAS.md                   # Template para respostas
```

---

## Dataset: clientes_campanha.csv

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| cliente_id | int | Identificador único |
| idade | int | Idade do cliente (18-80) |
| renda_mensal | float | Renda em R$ (1000-50000) |
| tempo_conta_meses | int | Meses como cliente (1-240) |
| num_produtos | int | Quantidade de produtos contratados (1-5) |
| tem_cartao_credito | int | 0 ou 1 |
| score_credito | float | Score de crédito (300-850) |
| respondeu_campanha | int | **Target:** 0 = não, 1 = sim |

---

## Tarefas

### Parte 1: Carregar e Explorar (pipeline/carregar.py)

Completar os TODOs para:
- Carregar o CSV
- Mostrar informações básicas (shape, tipos, head)
- Verificar distribuição da variável target

### Parte 2: Validar Dados (pipeline/validar.py)

Completar os TODOs para criar schema Pandera com:
- `cliente_id`: inteiro, não nulo, único
- `idade`: inteiro entre 18 e 80
- `renda_mensal`: float entre 1000 e 50000
- `score_credito`: float entre 300 e 850
- `respondeu_campanha`: inteiro, valores 0 ou 1

### Parte 3: Treinar Modelo (pipeline/treinar.py)

Completar os TODOs para:
- Separar features (X) e target (y)
- Fazer train-test split (80/20)
- Treinar RandomForestClassifier

### Parte 4: Executar e Interpretar (main.py + RESPOSTAS.md)

- Executar o pipeline completo
- Registrar F1-Score obtido
- Responder às perguntas de interpretação

---

## Requisitos de Entrega

### 1. Repositório Git
- Repositório com código funcionando
- **Mínimo 4 commits** com mensagens descritivas
- Sugestão de commits:
  1. "Implementa carregamento de dados"
  2. "Adiciona validação Pandera"
  3. "Implementa treinamento com train-test split"
  4. "Completa pipeline e documenta resultados"

### 2. Arquivo RESPOSTAS.md Preenchido
Todas as perguntas respondidas (template fornecido).

### 3. Pipeline Funcionando
Executar `python main.py` sem erros e gerar output com métricas.

---

## Critérios de Avaliação

| Critério | Peso |
|----------|------|
| Pipeline funciona sem erros | 30% |
| Validações Pandera corretas | 25% |
| Histórico Git adequado (4+ commits descritivos) | 20% |
| Respostas conceituais corretas | 25% |

---

## Dicas

- Executem o código **antes** de commitar para garantir que funciona
- Mensagens de commit devem descrever O QUE foi feito, não COMO
- Para validações Pandera, revisem os exemplos da Aula 2
- F1-Score esperado: entre 0.40 e 0.60 (dataset desbalanceado é normal)

---

## Prazo e Formato de Entrega

- **Formato:** Link para repositório GitHub (público ou com acesso ao professor)
- **Integrantes:** 2-4 pessoas por grupo

---

Bom trabalho!
