# 🔍 Guia de Debugging e Logs

Este guia mostra como usar o debugger do VS Code e implementar logs estruturados.

## 📋 Índice

1. [Debugger do VS Code](#debugger-do-vs-code)
2. [Logs Estruturados](#logs-estruturados)
3. [Comparação: Print vs Logger](#comparação-print-vs-logger)
4. [Exemplo Prático: Bug de Centavos](#exemplo-prático-bug-de-centavos)

---

## 🐛 Debugger do VS Code

### Passo 1: Configurar o Debugger

Crie o arquivo `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI Debug",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

### Passo 2: Usar Breakpoints

1. **Adicionar breakpoint**: Clique na margem esquerda da linha de código
2. **Iniciar debug**: Pressione `F5` ou clique em "Run and Debug"
3. **Inspecionar variáveis**: Passe o mouse sobre variáveis ou use o painel "Variables"
4. **Navegação**:
   - `F10`: Próxima linha (step over)
   - `F11`: Entrar na função (step into)
   - `Shift+F11`: Sair da função (step out)
   - `F5`: Continuar até próximo breakpoint

### Quando Usar o Debugger

✅ **Use debugger para:**
- Bugs lógicos (resultado inesperado)
- Entender fluxo de código complexo
- Inspecionar valores de variáveis em tempo real
- Desenvolvimento local

❌ **NÃO use debugger para:**
- Produção (use logs!)
- Problemas de performance
- Bugs intermitentes

---

## 📊 Logs Estruturados

### Por Que Logs Estruturados?

| Aspecto | Print | Logs Estruturados |
|---------|-------|-------------------|
| **Formato** | Texto livre | JSON |
| **Indexável** | ❌ Não | ✅ Sim |
| **Consultável** | ❌ Não | ✅ Sim |
| **Alertas** | ❌ Não | ✅ Sim |
| **Contexto** | ❌ Limitado | ✅ Rico |
| **Produção** | ❌ Não | ✅ Sim |

### Implementação

```python
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

def log_structured(level: str, event: str, **kwargs):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "event": event,
        **kwargs
    }
    
    if level == "ERROR":
        logger.error(json.dumps(log_entry))
    elif level == "WARNING":
        logger.warning(json.dumps(log_entry))
    else:
        logger.info(json.dumps(log_entry))
```

### Exemplo de Uso

```python
# ❌ Print (ruim para produção)
print("Transação recebida")

# ✅ Log estruturado (ideal para produção)
log_structured(
    "INFO",
    "transaction_received",
    valor=transacao.valor,
    user_id="usr_12345",
    request_id="req_abc789"
)
```

### Saída do Log

```json
{
  "timestamp": "2024-11-13T14:35:22Z",
  "level": "INFO",
  "event": "transaction_received",
  "valor": 15000,
  "user_id": "usr_12345",
  "request_id": "req_abc789"
}
```

---

## 🆚 Comparação: Print vs Logger

### Cenário 1: Erro de Validação

#### ❌ Com Print
```python
try:
    if valor <= 0:
        print("ERRO! Valor inválido")
        raise ValueError("Valor deve ser positivo")
except Exception as e:
    print(f"Erro: {e}")
```

**Problemas:**
- Sem timestamp
- Sem contexto (qual valor? qual usuário?)
- Não indexável
- Não gera alertas
- Inútil para diagnóstico em produção

#### ✅ Com Logger
```python
try:
    if valor <= 0:
        log_structured(
            "ERROR",
            "validation_failed",
            error_type="ValueError",
            error_message="Valor deve ser positivo",
            input_valor=valor,
            user_id=user_id,
            request_id=request_id
        )
        raise ValueError("Valor deve ser positivo")
except Exception as e:
    log_structured(
        "ERROR",
        "unexpected_error",
        error_type=type(e).__name__,
        error_message=str(e),
        stack_trace=traceback.format_exc()
    )
```

**Benefícios:**
- ✅ Timestamp automático
- ✅ Contexto completo
- ✅ Indexável no CloudWatch/Datadog
- ✅ Pode gerar alertas automáticos
- ✅ Rastreável por user_id ou request_id

---

## 🐛 Exemplo Prático: Bug de Centavos

### O Bug

Cliente reclama: "Transações com centavos estão sendo processadas incorretamente!"

### Investigação com Debugger

1. **Adicionar breakpoint** na linha de processamento:
   ```python
   valor_processado = int(transacao.valor)  # ← Breakpoint aqui
   ```

2. **Rodar com debugger** (F5)

3. **Enviar teste** com valor `10.50`

4. **Inspecionar variável**:
   - `transacao.valor` = `10.5` ✅
   - `valor_processado` = `10` ❌ BUG ENCONTRADO!

5. **Causa raiz**: `int()` trunca valores decimais

### A Correção

```python
# ❌ ANTES (bug)
valor_processado = int(transacao.valor)  # int(10.50) = 10

# ✅ DEPOIS (corrigido)
valor_processado = float(transacao.valor)  # float(10.50) = 10.50
```

### Testando a Correção

```bash
# Terminal 1: Rodar versão bugada
cd 3-exemplo-bug
uvicorn main_bug:app --reload --port 8000

# Terminal 2: Testar
curl -X POST http://localhost:8000/analisar \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 10.50,
    "hora_do_dia": 14,
    "distancia_ultima_compra_km": 100,
    "numero_transacoes_hoje": 5,
    "idade_conta_dias": 100
  }'

# Resultado: {"valor_processado": 10} ❌

# Rodar versão corrigida
uvicorn main_corrigido:app --reload --port 8000

# Testar novamente
# Resultado: {"valor_processado": 10.5} ✅
```

---

## 📈 Níveis de Log

Use os níveis apropriados:

| Nível | Quando Usar | Exemplo |
|-------|-------------|---------|
| **DEBUG** | Detalhes técnicos | "Conectando ao banco de dados" |
| **INFO** | Eventos normais | "Transação aprovada" |
| **WARNING** | Potenciais problemas | "Valor alto detectado" |
| **ERROR** | Erros recuperáveis | "Validação falhou" |
| **CRITICAL** | Erros fatais | "Banco de dados inacessível" |

---

## 🎯 Boas Práticas

### ✅ Faça

1. **Use logs estruturados em JSON** em produção
2. **Inclua contexto rico**: user_id, request_id, valores relevantes
3. **Use níveis apropriados**: INFO, WARNING, ERROR
4. **Log eventos importantes**: autenticação, transações, erros
5. **Use debugger** para desenvolvimento local

### ❌ Não Faça

1. **Não use print()** em produção
2. **Não logue senhas ou dados sensíveis**
3. **Não logue demais** (performance)
4. **Não use debugger** em produção
5. **Não ignore exceções** sem logar

---

## 🔗 Integração com Ferramentas

### CloudWatch (AWS)

```python
# Logs estruturados são automaticamente indexados
# Query no CloudWatch:
# fields @timestamp, event, valor, user_id
# | filter event = "fraud_detected"
# | sort @timestamp desc
```

### Datadog

```python
# Configurar Datadog handler
from datadog import statsd

log_structured(
    "ERROR",
    "fraud_detected",
    valor=15000,
    user_id="usr_123"
)

# Datadog cria métricas e alertas automáticos
statsd.increment('fraud.detected')
```

### Elastic Stack

```python
# Logs JSON são indexados automaticamente
# Kibana permite queries:
# event:"fraud_detected" AND valor:>10000
```

---

## 🚨 Alertas Automáticos

Exemplo de alerta baseado em logs:

```yaml
# CloudWatch Alarm
AlarmName: "High-Fraud-Rate"
MetricName: "fraud_detected_count"
Threshold: 10
EvaluationPeriods: 1
ComparisonOperator: "GreaterThanThreshold"
Actions:
  - "arn:aws:sns:us-east-1:123456789:fraud-alerts"
```

Quando logs estruturados detectam `event: "fraud_detected"` mais de 10 vezes em 1 minuto, o time de segurança recebe alerta!

---

## 📚 Recursos Adicionais

- [VS Code Debugging](https://code.visualstudio.com/docs/python/debugging)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Structured Logging Best Practices](https://www.structlog.org/)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
