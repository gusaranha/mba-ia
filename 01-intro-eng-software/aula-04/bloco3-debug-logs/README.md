# Bloco 3: Debug e Observabilidade

Este bloco demonstra técnicas de diagnóstico e observabilidade em aplicações de produção.

## 📁 Estrutura

```
bloco3-debug-logs/
├── 1-sem-logs/          # API sem logging estruturado
├── 2-com-logs/          # API com logging estruturado (JSON)
├── 3-exemplo-bug/       # Demonstração de debugging
└── como-debugar.md      # Guia de debugging
```

## 🎯 Objetivos

- Entender a diferença entre print() e logging estruturado
- Implementar logs JSON para produção
- Usar o debugger do VS Code para encontrar bugs lógicos
- Criar observabilidade em APIs

## 🚀 Como Usar

### 1. Sem Logs (Exemplo Ruim)
```bash
cd 1-sem-logs
uvicorn main:app --reload
```

### 2. Com Logs Estruturados (Exemplo Bom)
```bash
cd 2-com-logs
uvicorn main:app --reload
```

### 3. Exemplo de Bug
```bash
cd 3-exemplo-bug
# Testar versão com bug
uvicorn main_bug:app --reload

# Testar versão corrigida
uvicorn main_corrigido:app --reload
```

## 📊 Testando

Acesse `http://localhost:8000/docs` e teste o endpoint `/analisar` com:

```json
{
  "valor": 15000,
  "hora_do_dia": 3,
  "distancia_ultima_compra_km": 850,
  "numero_transacoes_hoje": 12,
  "idade_conta_dias": 45
}
```

## 🔍 O Que Observar

### Sem Logs
- Mensagens genéricas no terminal
- Difícil rastrear problemas
- Sem contexto sobre erros

### Com Logs
- Logs estruturados em JSON
- Contexto completo (timestamp, level, event, details)
- Fácil integração com CloudWatch/Datadog
- Alertas automáticos possíveis

## 💡 Conceitos Principais

1. **Print vs Logger**: Print é para desenvolvimento, Logger é para produção
2. **Logs Estruturados**: JSON permite indexação e busca
3. **Níveis de Log**: DEBUG, INFO, WARNING, ERROR, CRITICAL
4. **Contexto**: Sempre inclua informações relevantes (user_id, request_id, etc.)
