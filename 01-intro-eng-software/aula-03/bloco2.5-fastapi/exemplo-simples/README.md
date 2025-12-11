# Exemplo Simples - API com Validação

## Executar
```bash
uvicorn main:app --reload
```

## Testar

**Documentação interativa:**
```
http://localhost:8000/docs
```

**Caso válido:**
```json
{
  "nome": "Notebook",
  "preco": 2500.00,
  "estoque": 10,
  "ativo": true
}
```

**Casos inválidos (teste no /docs):**

1. Nome muito curto:
```json
{"nome": "PC", "preco": 100, "estoque": 5}
```
→ Erro: nome deve ter mínimo 3 caracteres

2. Preço negativo:
```json
{"nome": "Mouse", "preco": -10, "estoque": 5}
```
→ Erro: preço deve ser positivo

3. Estoque negativo:
```json
{"nome": "Teclado", "preco": 150, "estoque": -5}
```
→ Erro: estoque não pode ser negativo

## O Que Observar

- Pydantic valida **automaticamente**
- Erros retornam **422** com detalhes
- Documentação Swagger **gerada automaticamente**
- Type hints funcionam como **validação**
