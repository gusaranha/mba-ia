# Calculadora de Frete

Calcula valor de frete baseado em peso e distância.

## Regra de Negócio

**Frete = (Peso × R$ 10) + (Distância × R$ 0,50)**

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
  "peso": 5.0,
  "distancia": 100
}
```

**Resposta:**
```json
{
  "valor_frete": 100.0
}
```

**Cálculo:** (5kg × 10) + (100km × 0.5) = 50 + 50 = **R$ 100**

## Testes

```bash
pytest tests/ -v
```
