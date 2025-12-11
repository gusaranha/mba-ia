# Validador de CPF

Valida CPF de forma simplificada.

## Regra de Validação

- Remove pontos e traços
- Verifica se tem exatamente 11 dígitos
- Verifica se todos são numéricos

## Como Executar

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

Acesse: http://localhost:8000/docs

## Exemplo de Uso

```json
POST /validar
{
  "cpf": "123.456.789-00"
}
```

**Resposta:**
```json
{
  "cpf": "123.456.789-00",
  "valido": true
}
```

## Testes

```bash
pytest tests/ -v
```

## Casos de Teste

- ✅ CPF formatado: "123.456.789-00"
- ✅ CPF sem formatação: "12345678900"
- ❌ CPF curto: "123"
- ❌ CPF com letras: "123.456.789-AB"
