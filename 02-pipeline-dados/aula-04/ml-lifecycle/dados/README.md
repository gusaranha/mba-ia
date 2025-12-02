# Dados de Transações Bancárias 2025

## Origem dos Dados

Estes dados simulam transações bancárias reais de um banco brasileiro.

### Outubro 2025 (`outubro_2025.csv`)
- **Período**: 01/10/2025 - 31/10/2025
- **Total**: 2000 transações
- **Taxa de fraude**: 10% (200 fraudes)
- **Uso**: Treino do modelo inicial (v1.0)

**Padrões de fraude em Outubro:**
- Valores altos (>R$ 3.000)
- Madrugada/noite (0-6h, 22-23h)
- Categorias: eletrônicos, joias
- Múltiplas transações (>10 em 24h)

### Novembro 2025 (`novembro_2025.csv`)
- **Período**: 01/11/2025 - 30/11/2025
- **Total**: 2000 transações
- **Taxa de fraude**: 15% (300 fraudes) ⬆️
- **Uso**: Dados de produção (detectar degradação)

**MUDANÇAS vs Outubro:**
- ⚠️ Taxa de fraude aumentou 50%
- ⚠️ Fraudes agora em horário comercial
- ⚠️ Novas categorias: PIX, Transferência
- ⚠️ Valores médios subiram ~35%

## Estrutura dos Dados

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `transaction_id` | string | ID único da transação |
| `data` | string | Período (2025-10 ou 2025-11) |
| `valor` | float | Valor em R$ |
| `hora` | int | Hora da transação (0-23) |
| `categoria` | string | Categoria do estabelecimento |
| `categoria_cod` | int | Código numérico da categoria |
| `qtd_transacoes_24h` | int | Quantidade de transações nas últimas 24h |
| `is_fraud` | int | 0=legítima, 1=fraude |

## Categorias

1. alimentacao
2. farmacia
3. transporte
4. vestuario
5. restaurante
6. lazer
7. eletronicos
8. livros
9. assinatura
10. supermercado
11. joias
12. viagem
13. pix (nova em Nov)
14. transferencia (nova em Nov)

---

**Nota**: Estes dados são sintéticos, gerados para fins educacionais. 
Em produção real, viriam de sistemas bancários legados via ETL.
