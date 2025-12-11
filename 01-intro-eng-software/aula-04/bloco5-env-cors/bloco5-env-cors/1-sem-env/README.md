# ❌ Exemplo 1: SEM Variáveis de Ambiente

## 🎯 Objetivo

Mostrar os **problemas** de ter configurações hardcoded no código.

---

## ❌ Problemas Deste Código

### 1. Configurações Fixas

```python
APP_NAME = "Fraud Detection API"
MODEL_PATH = "artifacts/models/fraud_detection_model.pkl"
LOG_LEVEL = "INFO"
FRAUD_THRESHOLD = 10000
```

**Problema**: Para mudar qualquer configuração, tem que **alterar o código**!

### 2. Sem Diferenciação de Ambientes

- Desenvolvimento usa as mesmas configs de produção
- Não tem como ter LOG_LEVEL diferente por ambiente

### 3. Risco de Segurança

Se tivesse senhas ou tokens:

```python
DATABASE_URL = "postgresql://user:senha123@localhost/db"  # ❌ PÉSSIMO!
API_KEY = "sk-abc123xyz"  # ❌ VAI PRO GIT!
```

**Problema**: Segredos seriam versionados no Git!

### 4. Difícil de Manter

- Cada desenvolvedor tem que mudar o código para seu ambiente
- Produção precisa de deploy só para mudar uma config

---

## 🚀 Como Rodar

### 1. Instalar Dependências

```bash
pip install fastapi uvicorn
```

### 2. Rodar a API

```bash
# Na pasta 1-sem-env/
uvicorn main:app --reload
```

### 3. Acessar

- Docs: http://localhost:8000/docs
- Config: http://localhost:8000/config

---

## 🧪 Testando o Problema

### Ver Configurações Hardcoded

```bash
curl http://localhost:8000/config
```

**Resposta:**

```json
{
  "app_name": "Fraud Detection API",
  "version": "1.0.0",
  "model_path": "artifacts/models/fraud_detection_model.pkl",
  "log_level": "INFO",
  "fraud_threshold": 10000,
  "warning": "Todas essas configs estão HARDCODED no código!"
}
```

### Testar Predição

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 15000,
    "hora_do_dia": 14,
    "distancia_ultima_compra_km": 100,
    "numero_transacoes_hoje": 5,
    "idade_conta_dias": 90
  }'
```

### Problema: Mudar o Threshold

**Cenário**: O gerente pediu para mudar o threshold de R$ 10.000 para R$ 15.000.

**Solução atual**: ❌ Alterar o código, commitar, fazer deploy!

```python
FRAUD_THRESHOLD = 15000  # Mudou código!
```

**Problema**:

- Deploy desnecessário
- Risco de introduzir bugs
- Processo lento

---

## 📊 Comparação

| Aspecto                   | Sem .env       | Com .env           |
| ------------------------- | -------------- | ------------------ |
| **Mudar config**          | Alterar código | Alterar arquivo    |
| **Deploy necessário?**    | ✅ Sim          | ❌ Não (só restart) |
| **Segredos seguros?**     | ❌ Não          | ✅ Sim              |
| **Ambientes diferentes?** | ❌ Difícil      | ✅ Fácil            |

---

## 
