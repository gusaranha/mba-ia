# Como Usar - MLflow Demos

Demonstrações e exercícios de MLflow para rastreamento de experimentos de ML.

### Estrutura
```
mlflow_demos/
├── data/
│   ├── transacoes_processadas.csv    ✅ Dados prontos (2000 registros)
│   └── README.txt
├── demos/
│   ├── demo_1_treinar_com_mlflow.py  Treino básico + MLflow
│   ├── demo_2_multiplos_experimentos.py  13 experimentos
│   └── demo_3_carregar_modelo.py     Buscar e usar modelo
├── exercicios/
│   ├── exercicio_1_mlflow_basico.py
│   ├── exercicio_opcional_multiplos.py
│   └── gabaritos/
└── requirements.txt
```

##  Setup

```bash
# Instalar dependências
pip install -r requirements.txt
```

Os dados estão em `data/transacoes_processadas.csv`


### Demo 1: Treino Básico (5min)
```bash
cd demos
python demo_1_treinar_com_mlflow.py

# Em outro terminal
mlflow ui --host 127.0.0.1 --port 5000
# Abrir http://localhost:5000
```

### Demo 2: Múltiplos Experimentos (5min)
```bash
python demo_2_multiplos_experimentos.py
# Atualizar MLflow UI (F5)
# Ordenar por f1_score
# Comparar runs
```

### Demo 3: Carregar Modelo (5min)
```bash
python demo_3_carregar_modelo.py
# Mostra como buscar melhor modelo
# Carrega e faz predições
```

### Exercícios (20-30min)
```bash
cd ../exercicios

# Exercício 1: Alunos completam TODOs
# Gabarito em: gabaritos/exercicio_1_gabarito.py

# Exercício opcional (avançado)
# Gabarito em: gabaritos/exercicio_opcional_gabarito.py
```

