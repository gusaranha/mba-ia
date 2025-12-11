# ✅ Exemplo 2: COM Variáveis de Ambiente

## 🎯 Objetivo

Mostrar como usar variáveis de ambiente para configuração externa e segura.

---

## ✅ Soluções Deste Código

### 1. Configurações Externas

```python
# Código lê do .env
APP_NAME = os.getenv("APP_NAME", "Fraud Detection API")
FRAUD_THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", "10000"))
```

**Solução**: Muda só o arquivo .env, não o código!

### 2. Ambientes Diferentes

- Desenvolvimento: .env com LOG_LEVEL=DEBUG
- Produção: .env com LOG_LEVEL=ERROR

### 3. Segredos Protegidos

```python
# .env (NÃO vai pro Git)
DATABASE_URL=postgresql://user:senha123@localhost/db

# .env.example (VAI pro Git)
DATABASE_URL=
```

**Solução**: Segredos ficam só no .env local!

### 4. Fácil de Manter

- Cada dev tem seu .env personalizado
- Produção muda configs sem deploy

---

## 🚀 Como Rodar

### 1. Instalar Dependências

```bash
pip install fastapi uvicorn python-dotenv
```

### 2. Criar Arquivo .env

```bash
# Na pasta 2-com-env/
cp .env.example .env
```

### 3. Editar .env (Opcional)

Abra `.env` e ajuste os valores:

```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
FRAUD_THRESHOLD=15000
```

### 4. Rodar a API

```bash
uvicorn main:app --reload
```

### 5. Acessar

- Docs: http://localhost:8000/docs
- Config: http://localhost:8000/config

---

## 🧪 Testando a Solução

### Ver Configurações do .env

```bash
curl http://localhost:8000/config
```

**Resposta:**

```json
{
  "app_name": "Fraud Detection API",
  "version": "1.0.0",
  "environment": "development",
  "model_path": "artifacts/models/fraud_detection_model.pkl",
  "log_level": "DEBUG",
  "fraud_threshold": 10000,
  "message": "✅ Todas essas configs vêm do arquivo .env!"
}
```

### Mudar o Threshold SEM Alterar Código

**1. Edite o .env:**

```env
FRAUD_THRESHOLD=15000
```

**2. Reinicie a API:**

```bash
# Ctrl+C e rodar novamente
uvicorn main:app --reload
```

**3. Verifique:**

```bash
curl http://localhost:8000/config
```

**Resultado**: Threshold mudou para 15000! ✅

### Testar Predição

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 12000,
    "hora_do_dia": 14,
    "distancia_ultima_compra_km": 100,
    "numero_transacoes_hoje": 5,
    "idade_conta_dias": 90
  }'
```

---

## 📂 Arquivos Importantes

### .env.example

- ✅ Template vazio (sem segredos)
- ✅ VAI para o Git
- ✅ Documenta todas as variáveis necessárias

### .env

- ❌ Arquivo real com valores (com segredos)
- ❌ NÃO VAI para o Git (.gitignore)
- ✅ Cada desenvolvedor tem o seu

### .gitignore

- ✅ Garante que .env não vai pro Git
- ✅ Protege segredos

---

## 🔒 Segurança

### O Que Vai pro Git?

✅ `.env.example` (template vazio)  
✅ `.gitignore` (ignora .env)  
✅ `main.py` (código sem segredos)  
❌ `.env` (arquivo real com valores)

### Workflow Seguro

1. Desenvolvedor clona projeto
2. Copia `.env.example` para `.env`
3. Preenche valores reais no `.env`
4. `.env` fica só na máquina local
5. Segredos protegidos! ✅

---

## 📊 Comparação

| Cenário                        | Sem .env                | Com .env              |
| ------------------------------ | ----------------------- | --------------------- |
| **Mudar threshold**            | Alterar código + deploy | Editar .env + restart |
| **Dev tem valores diferentes** | Conflitos no Git        | Cada um tem seu .env  |
| **Senhas seguras**             | ❌ Vão pro Git           | ✅ Só no .env local    |
| **Múltiplos ambientes**        | Difícil                 | Fácil                 |

---

## 💡 Boas Práticas

### ✅ Faça

- Use `.env` para TODAS as configurações
- Sempre crie `.env.example`
- Adicione `.env` no `.gitignore`
- Use valores padrão no `os.getenv()`

### ❌ Não Faça

- Nunca commite `.env`
- Nunca coloque senhas no código
- Nunca coloque senhas no `.env.example`
- Nunca use configurações hardcoded

---



---

## 🎓 Exercício

**Desafio**: Adicione uma nova variável de ambiente

1. Adicione no `.env.example`:
   
   ```env
   MAX_REQUESTS_PER_MINUTE=60
   ```

2. Adicione no `.env`:
   
   ```env
   MAX_REQUESTS_PER_MINUTE=60
   ```

3. Leia no código:
   
   ```python
   MAX_REQUESTS = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
   ```

4. Use onde necessário!

---

**Parabéns!** Agora você sabe usar variáveis de ambiente! 🎉
