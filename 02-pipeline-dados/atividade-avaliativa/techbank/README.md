# Trabalho: Pipeline de ML - Campanha de Marketing

## Descrição
Pipeline de classificação para prever quais clientes responderão a uma campanha de marketing do TechBank.

## Estrutura do Projeto
```
trabalho_grupo/
├── data/
│   └── clientes_campanha.csv   # Dataset
├── pipeline/
│   ├── carregar.py             # Etapa 1: Carregar dados
│   ├── validar.py              # Etapa 2: Validar dados
│   ├── treinar.py              # Etapa 3: Treinar modelo
│   └── avaliar.py              # Etapa 4: Avaliar modelo
├── models/                      # Modelos salvos
├── main.py                      # Script principal
├── requirements.txt             # Dependências
└── RESPOSTAS.md                 # Suas respostas
```

## Como Executar

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Completar os TODOs nos arquivos:
   - `pipeline/carregar.py`
   - `pipeline/validar.py`
   - `pipeline/treinar.py`

3. Executar o pipeline:
```bash
python main.py
```

4. Preencher `RESPOSTAS.md` com os resultados

## Entrega
- Repositório Git com código funcionando
- Mínimo 4 commits descritivos
- Arquivo RESPOSTAS.md preenchido
