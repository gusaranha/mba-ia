# Template - API Base

## 🎯 Use este template como ponto de partida!

Este é um template básico com a estrutura profissional pronta.

## Estrutura

```
template/
├── src/
│   ├── api/
│   │   └── main.py          # Endpoints da API
│   ├── models/
│   │   └── schemas.py       # Modelos Pydantic
│   └── config.py            # Configurações
├── tests/
│   └── test_template.py     # Testes automatizados
├── requirements.txt
└── .gitignore
```

## Como Usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Rodar a API

```bash
uvicorn src.api.main:app --reload
```

### 3. Acessar documentação

http://localhost:8000/docs

### 4. Rodar testes

```bash
pytest tests/ -v
```

## 🔧 Customização

### Passo 1: Adapte os Schemas

Edite `src/models/schemas.py` com seus modelos de dados.

### Passo 2: Implemente sua Lógica

Edite `src/api/main.py` e substitua a lógica do endpoint `/calcular`.

### Passo 3: Crie Testes

Edite `tests/test_template.py` para testar sua lógica.

## Exemplo Atual

API de soma simples:
- **POST /calcular**: Soma dois números

Substitua isso pela sua lógica de negócio!
