# Dados de Transações - Detecção de Fraudes

Este arquivo contém 2000 transações bancárias já processadas e prontas para uso.

## Origem
Em produção real, estes dados viriam de sistemas bancários via ETL.
Para fins educacionais, foram gerados sinteticamente com padrões realistas.

## Estrutura
- valor: Valor da transação em R$
- hora: Hora da transação (0-23)
- categoria_cod: Código da categoria (1-5)
- qtd_transacoes_24h: Quantidade de transações nas últimas 24h
- is_fraud: 0=legítima, 1=fraude

## Uso
Basta carregar o CSV:
```python
import pandas as pd
df = pd.read_csv("data/transacoes_processadas.csv")
```

