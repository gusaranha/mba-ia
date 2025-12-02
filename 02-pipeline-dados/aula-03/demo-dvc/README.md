# Demo DVC - Projeto Independente

Projeto isolado para demonstração do DVC (Data Version Control).

## Estrutura

```
demo-dvc/
├── gerar_dados.py       # Gera dados sintéticos
├── treinar_modelo.py    # Job de re-treinamento
├── ROTEIRO.md           # Passo a passo para demonstração
├── requirements.txt
├── data/                # Dados (gerados)
└── models/arquivo/      # Modelos arquivados
```

## Como usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Gerar dados
```bash
python gerar_dados.py
```

### 3. Seguir o roteiro
Abra `ROTEIRO.md` e siga o passo a passo.

## Tempo estimado

- Preparação: 2 min
- Parte 1 (Setup): 5 min
- Parte 2 (Dados v1): 10 min
- Parte 3 (Modelo v1): 5 min
- Parte 4 (Nova semana): 10 min
- Parte 5 (Navegar): 10 min
- Parte 6 (Resumo): 2 min

**Total: ~45 min**
