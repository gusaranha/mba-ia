# 📖 Guia Completo: Variáveis de Ambiente

## 📚 Índice

1. [O Que São Variáveis de Ambiente](#o-que-são)
2. [Por Que Usar](#por-que-usar)
3. [Como Usar em Python](#como-usar-python)
4. [Boas Práticas](#boas-práticas)
5. [.env vs .env.example](#env-vs-envexample)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 O Que São Variáveis de Ambiente? {#o-que-são}

Variáveis de ambiente são **configurações externas** ao código que definem como sua aplicação deve se comportar.

### Analogia

Imagine uma TV:

- **Sem variáveis de ambiente**: Abrir a TV e soldar componentes para mudar o canal
- **Com variáveis de ambiente**: Usar o controle remoto

### Tecnicamente

```python
# ❌ Hardcoded
database_url = "postgresql://user:senha@localhost/db"

# ✅ Variável de ambiente
database_url = os.getenv("DATABASE_URL")
```

---

## 🤔 Por Que Usar? {#por-que-usar}

### 1. Segurança 🔒

```python
# ❌ NUNCA faça isso
API_KEY = "sk-abc123xyz"  # VAI PRO GIT!

# ✅ Use variável de ambiente
API_KEY = os.getenv("API_KEY")  # .env não vai pro Git
```

### 2. Flexibilidade ⚙️

```env
# Desenvolvimento
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///dev.db

# Produção
LOG_LEVEL=ERROR
DATABASE_URL=postgresql://prod-server/db
```

### 3. Facilidade 🚀

Mude configurações **sem alterar código**:

- Edita `.env`
- Reinicia aplicação
- Pronto!

### 4. Colaboração 👥

Cada desenvolvedor tem seu próprio `.env`:

```
dev-1: DATABASE_URL=localhost
dev-2: DATABASE_URL=192.168.1.100
```

Sem conflitos no Git!

---

## 💻 Como Usar em Python {#como-usar-python}

### Método 1: os.getenv() (Nativo)

```python
import os

# Ler variável
api_key = os.getenv("API_KEY")

# Com valor padrão
port = os.getenv("PORT", "8000")

# Converter para int
port = int(os.getenv("PORT", "8000"))
```

### Método 2: python-dotenv (Recomendado)

**Instalar:**

```bash
pip install python-dotenv
```

**Usar:**

```python
from dotenv import load_dotenv
import os

# Carregar .env
load_dotenv()

# Usar normalmente
api_key = os.getenv("API_KEY")
```

### Vantagens do python-dotenv

- ✅ Lê arquivo `.env` automaticamente
- ✅ Suporta comentários no `.env`
- ✅ Variáveis do sistema têm prioridade
- ✅ Funciona em qualquer ambiente

---

## ✅ Boas Práticas {#boas-práticas}

### 1. Sempre Use Valores Padrão

```python
# ❌ Ruim (pode dar erro)
port = int(os.getenv("PORT"))

# ✅ Bom (sempre funciona)
port = int(os.getenv("PORT", "8000"))
```

### 2. Organize por Categoria

```env
# ========================================
# APLICAÇÃO
# ========================================
APP_NAME=My API
ENVIRONMENT=development

# ========================================
# BANCO DE DADOS
# ========================================
DATABASE_URL=postgresql://...
DATABASE_POOL_SIZE=10

# ========================================
# SEGREDOS
# ========================================
SECRET_KEY=...
```

### 3. Use UPPER_CASE

```env
# ✅ Correto
DATABASE_URL=...
API_KEY=...

# ❌ Evite
database_url=...
apiKey=...
```

### 4. Nunca Commite .env

```bash
# .gitignore
.env
.env.local
*.env
```

### 5. Sempre Crie .env.example

```env
# .env.example
DATABASE_URL=
API_KEY=
SECRET_KEY=
```

---

## 📄 .env vs .env.example {#env-vs-envexample}

### .env

- ❌ **NÃO VAI** para o Git
- ✅ Contém valores **reais**
- ✅ Pode ter **segredos**
- ✅ **Cada desenvolvedor** tem o seu

```env
# .env (local, não versionado)
DATABASE_URL=postgresql://user:senha123@localhost/db
API_KEY=sk-abc123xyz
```

### .env.example

- ✅ **VAI** para o Git
- ✅ Template **vazio**
- ❌ **SEM segredos**
- ✅ Documenta variáveis necessárias

```env
# .env.example (versionado)
DATABASE_URL=
API_KEY=
```

### Workflow

```bash
# 1. Desenvolvedor clona projeto
git clone ...

# 2. Copia template
cp .env.example .env

# 3. Preenche valores reais
vim .env

# 4. Roda aplicação
python app.py
```

---

## 🧪 Exemplos Práticos {#exemplos-práticos}

### Exemplo 1: Configuração Simples

**.env:**

```env
APP_NAME=My API
DEBUG=True
PORT=8000
```

**Código:**

```python
from dotenv import load_dotenv
import os

load_dotenv()

app_name = os.getenv("APP_NAME", "Default API")
debug = os.getenv("DEBUG", "False").lower() == "true"
port = int(os.getenv("PORT", "8000"))

print(f"Running {app_name} on port {port} (debug={debug})")
```

### Exemplo 2: Banco de Dados

**.env:**

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
DATABASE_POOL_SIZE=10
DATABASE_TIMEOUT=30
```

**Código:**

```python
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(
    os.getenv("DATABASE_URL"),
    pool_size=int(os.getenv("DATABASE_POOL_SIZE", "5")),
    pool_timeout=int(os.getenv("DATABASE_TIMEOUT", "30"))
)
```

### Exemplo 3: Múltiplos Ambientes

**Estrutura:**

```
projeto/
├── .env.development
├── .env.production
└── app.py
```

**.env.development:**

```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///dev.db
```

**.env.production:**

```env
ENVIRONMENT=production
LOG_LEVEL=ERROR
DATABASE_URL=postgresql://prod/db
```

**Código:**

```python
from dotenv import load_dotenv
import os

# Carregar env específico
env = os.getenv("ENV", "development")
load_dotenv(f".env.{env}")

# Usar configurações
log_level = os.getenv("LOG_LEVEL")
db_url = os.getenv("DATABASE_URL")
```

---

## 🔧 Troubleshooting {#troubleshooting}

### Problema 1: Variável Não Carrega

**Sintoma:**

```python
api_key = os.getenv("API_KEY")
print(api_key)  # None
```

**Solução:**

1. Verifique se chamou `load_dotenv()`
2. Verifique se o arquivo é `.env` (não `.env.txt`)
3. Verifique se está no diretório correto
4. Verifique se a variável existe no `.env`

### Problema 2: Arquivo .env Foi pro Git

**Solução:**

```bash
# 1. Remover do Git
git rm --cached .env

# 2. Adicionar no .gitignore
echo ".env" >> .gitignore

# 3. Commit
git commit -m "Remove .env from Git"
```

### Problema 3: Valor com Espaços

**Problema:**

```env
API_KEY=sk abc 123  # ❌ Espaços!
```

**Solução:**

```env
# Use aspas
API_KEY="sk abc 123"

# Ou sem espaços
API_KEY=sk_abc_123
```

### Problema 4: Variável Booleana

**Problema:**

```python
debug = os.getenv("DEBUG", "False")
if debug:  # ❌ Sempre True (string não vazia)
    ...
```

**Solução:**

```python
# Converter para bool
debug = os.getenv("DEBUG", "False").lower() == "true"

# Ou usar helper
def str_to_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")

debug = str_to_bool(os.getenv("DEBUG", "False"))
```

---

## 📚 Recursos Adicionais

### Documentação

- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [The Twelve-Factor App - Config](https://12factor.net/config)



- [ ] `.env` está no `.gitignore`
- [ ] `.env.example` documenta todas as variáveis
- [ ] Todas as variáveis têm valores padrão
- [ ] Nenhum segredo está hardcoded
- [ ] Testou em ambiente de staging
- [ ] Documentou variáveis obrigatórias
- [ ] Configurou variáveis no servidor de produção

---

## 🎓 Exercícios

### Exercício 1: Básico

Crie um `.env` com 3 variáveis e leia com `os.getenv()`.

### Exercício 2: Conversão

Leia uma variável numérica e converta para `int`.

### Exercício 3: Múltiplos Ambientes

Crie `.env.development` e `.env.production` com configs diferentes.

### Exercício 4: Validação

Crie função que valida se todas as variáveis obrigatórias existem.

---

**Continue estudando!** 🚀
