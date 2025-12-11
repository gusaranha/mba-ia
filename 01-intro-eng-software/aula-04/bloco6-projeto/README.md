# Bloco 5 - Projeto Final

## Objetivo

Construir sua própria API de Lógica de Negócio aplicando os 3 pilares da aula:
- 🔷 **Git**: Histórico de commits organizado
- 🔍 **Logs**: Observabilidade com logging estruturado
- ✅ **Testes**: Validação automatizada com pytest

## Estrutura do Projeto

```
bloco5-projeto/
├── template/          # Template inicial para começar
└── exemplos/          # 3 exemplos completos de referência
    ├── exemplo-pedidos/
    ├── exemplo-frete/
    └── exemplo-validador/
```

## Como Começar

### 1. Use o Template

```bash
cd template/
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

### 2. Adapte para Seu Projeto

- Substitua a lógica do endpoint `/calcular`
- Atualize os schemas em `src/models/schemas.py`
- Crie testes em `tests/`

### 3. Consulte os Exemplos

Se tiver dúvidas, consulte os 3 exemplos completos na pasta `exemplos/`

## Requisitos de Entrega

✅ **Repositório GitHub (Público)**
✅ **README.md** - Explicação do projeto e como rodar
✅ **API FastAPI** - Pelo menos 2 endpoints
✅ **Validação Pydantic** - Modelos claros
✅ **Testes pytest** - Mínimo 2 testes
✅ **Git** - Commits descritivos

## Temas Sugeridos

- 🛒 Sistema de pedidos (calcular total, desconto)
- 📦 Calculadora de frete (peso, distância)
- ✅ Validador (CPF, email, etc)
- 📝 CRUD simples (lista de tarefas)
- 💰 Calculadora financeira (juros, parcelas)

**Prazo:** 22/11/2025 (23h59)
