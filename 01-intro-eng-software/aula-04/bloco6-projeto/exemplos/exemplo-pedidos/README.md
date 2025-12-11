# Sistema de Pedidos

Calcula total de pedidos com desconto opcional.

## Funcionalidades

- Soma itens do pedido (quantidade × preço)
- Aplica desconto de 10% com cupom "DESC10"
- Retorna subtotal, desconto e total

## Como Executar

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

Acesse: http://localhost:8000/docs

## Exemplo de Uso

```json
POST /calcular
{
  "itens": [
    {"nome": "Mouse", "quantidade": 2, "preco": 50.0}
  ],
  "cupom": "DESC10"
}
```

**Resposta:**
```json
{
  "subtotal": 100.0,
  "desconto": 10.0,
  "total": 90.0
}
```

## Testes

```bash
pytest tests/ -v
```
