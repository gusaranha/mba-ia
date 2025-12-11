# 📖 Guia Completo: CORS

## 📚 Índice

1. [O Que é CORS](#o-que-é)
2. [Por Que CORS Existe](#por-que-existe)
3. [Como Funciona](#como-funciona)
4. [Configurando no FastAPI](#configurando-fastapi)
5. [Desenvolvimento vs Produção](#dev-vs-prod)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Troubleshooting](#troubleshooting)

---

## 🌐 O Que é CORS? {#o-que-é}

**CORS** = Cross-Origin Resource Sharing (Compartilhamento de Recursos entre Origens)

### Definição Simples

Política de segurança que determina **quais sites** podem chamar sua API.

### Origem (Origin)

Uma origem é definida por:

- **Protocolo**: http vs https
- **Domínio**: exemplo.com vs api.exemplo.com
- **Porta**: :80 vs :8000

### Exemplos de Origens Diferentes

```
http://localhost:3000  ≠  http://localhost:8000  (porta diferente)
http://meu-site.com    ≠  https://meu-site.com   (protocolo diferente)
http://api.site.com    ≠  http://www.site.com    (subdomínio diferente)
```

---

## 🔒 Por Que CORS Existe? {#por-que-existe}

### O Problema (Sem CORS)

**Cenário:**

1. Você visita `banco-seguro.com`
2. Site malicioso `banco-falso.com` faz requisição para `banco-seguro.com/transferir`
3. ❌ Seu dinheiro é transferido!

### A Solução (Com CORS)

Navegador pergunta:

> "API do banco-seguro.com, o site banco-falso.com pode te chamar?"

API responde:

> "Não! Só banco-seguro.com pode me chamar."

Navegador bloqueia a requisição! ✅

### Política Same-Origin

**Regra padrão dos navegadores:**

- Site X só pode chamar APIs da **mesma origem**
- Para chamar APIs de **outras origens**, precisa de CORS

---

## ⚙️ Como Funciona? {#como-funciona}

### Fluxo de Requisição com CORS

```
1. Frontend em http://meu-site.com faz requisição
   ↓
2. Navegador envia "Preflight Request" (OPTIONS)
   Headers:
   - Origin: http://meu-site.com
   - Access-Control-Request-Method: POST
   ↓
3. API responde com headers CORS
   Headers:
   - Access-Control-Allow-Origin: http://meu-site.com
   - Access-Control-Allow-Methods: GET, POST
   ↓
4. Navegador permite ou bloqueia
   ↓
5. Se permitido, requisição real é enviada
```

### Headers CORS Importantes

| Header                             | Descrição               | Exemplo                       |
| ---------------------------------- | ----------------------- | ----------------------------- |
| `Access-Control-Allow-Origin`      | Origens permitidas      | `*` ou `http://site.com`      |
| `Access-Control-Allow-Methods`     | Métodos HTTP permitidos | `GET, POST, PUT`              |
| `Access-Control-Allow-Headers`     | Headers permitidos      | `Content-Type, Authorization` |
| `Access-Control-Allow-Credentials` | Permite cookies/auth    | `true`                        |

---

## 🚀 Configurando no FastAPI {#configurando-fastapi}

### Básico

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Qualquer origem
    allow_credentials=True,
    allow_methods=["*"],           # Qualquer método
    allow_headers=["*"],           # Qualquer header
)
```

### Configuração Detalhada

```python
app.add_middleware(
    CORSMiddleware,

    # Origens permitidas
    allow_origins=[
        "http://localhost:3000",
        "https://meu-site.com"
    ],

    # Padrões de origens (regex)
    allow_origin_regex="https://.*\.meu-site\.com",

    # Permite cookies e autenticação
    allow_credentials=True,

    # Métodos HTTP permitidos
    allow_methods=["GET", "POST", "PUT", "DELETE"],

    # Headers permitidos
    allow_headers=["Content-Type", "Authorization"],

    # Headers expostos ao frontend
    expose_headers=["X-Custom-Header"],

    # Tempo de cache do preflight (segundos)
    max_age=3600,
)
```

### Com Variáveis de Ambiente

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Ler do .env
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**.env:**

```env
# Desenvolvimento
CORS_ORIGINS=*

# Produção
CORS_ORIGINS=https://meu-site.com,https://app.meu-site.com
```

---

## 🔄 Desenvolvimento vs Produção {#dev-vs-prod}

### Desenvolvimento

**Objetivo:** Facilitar testes

```python
allow_origins=["*"]
```

**Vantagens:**

- ✅ Qualquer frontend pode testar
- ✅ Sem configuração extra
- ✅ Rápido para desenvolver

**Desvantagens:**

- ⚠️ Inseguro
- ⚠️ Qualquer site pode acessar

**Uso:** Apenas local!

### Produção

**Objetivo:** Segurança máxima

```python
allow_origins=[
    "https://meu-site.com",
    "https://app.meu-site.com"
]
```

**Vantagens:**

- ✅ Seguro
- ✅ Controle total
- ✅ Apenas sites autorizados

**Desvantagens:**

- ⚠️ Precisa configurar cada domínio
- ⚠️ Precisa atualizar ao adicionar novos frontends

**Uso:** Sempre em produção!

### Tabela Comparativa

| Aspecto              | Dev (`*`)     | Prod (específico) |
| -------------------- | ------------- | ----------------- |
| **Segurança**        | ⚠️ Baixa      | ✅ Alta            |
| **Facilidade**       | ✅ Muito fácil | ⚠️ Requer config  |
| **Flexibilidade**    | ✅ Total       | ⚠️ Limitada       |
| **Recomendado para** | Local apenas  | Deploy real       |

---

## 🧪 Exemplos Práticos {#exemplos-práticos}

### Exemplo 1: API Pública

API que qualquer um pode chamar:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],  # Só leitura
    allow_headers=["*"],
)
```

**Uso:** APIs públicas de consulta (clima, CEP, etc)

### Exemplo 2: API Privada (SPA)

API só para seu Single Page Application:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.meu-site.com"],
    allow_credentials=True,  # Cookies de sessão
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**Uso:** Backend de aplicações web

### Exemplo 3: Múltiplos Frontends

```python
# Lista de frontends autorizados
ALLOWED_ORIGINS = [
    "https://www.meu-site.com",      # Site principal
    "https://app.meu-site.com",      # Aplicação web
    "https://admin.meu-site.com",    # Painel admin
    "https://mobile.meu-site.com",   # API para mobile web
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Exemplo 4: Regex para Subdomínios

Permitir todos os subdomínios:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.meu-site\.com",  # *.meu-site.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Permite:**

- ✅ https://app.meu-site.com
- ✅ https://admin.meu-site.com
- ✅ https://qualquer-coisa.meu-site.com

**Bloqueia:**

- ❌ https://meu-site.com (sem subdomínio)
- ❌ https://outro-site.com

---

## 🔧 Troubleshooting {#troubleshooting}

### Problema 1: "CORS policy" no Console

**Erro:**

```
Access to fetch at 'http://localhost:8000/api' from origin 
'http://localhost:3000' has been blocked by CORS policy
```

**Causas Possíveis:**

1. CORS não configurado
2. Origem não está na lista
3. Middleware não adicionado

**Solução:**

```python
# Verifique se o middleware está adicionado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adicione a origem
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problema 2: Cookies Não Funcionam

**Sintoma:**
Cookies não são enviados/recebidos entre frontend e API.

**Solução:**

```python
# 1. Habilite credentials no backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,  # ← IMPORTANTE
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Configure fetch no frontend
fetch('http://localhost:8000/api', {
    credentials: 'include'  // ← IMPORTANTE
})
```

### Problema 3: Preflight Falha

**Erro:**

```
Response to preflight request doesn't pass access control check
```

**Causa:**
Endpoint não responde a requisições OPTIONS.

**Solução:**
FastAPI já lida com OPTIONS automaticamente se CORS estiver configurado.

### Problema 4: "*" Não Funciona em Produção

**Problema:**
`allow_origins=["*"]` não funciona com `allow_credentials=True`.

**Motivo:**
Navegadores não permitem `*` com credentials por segurança.

**Solução:**

```python
# ❌ Não funciona
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Conflito!
)

# ✅ Funciona
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meu-site.com"],  # Específico
    allow_credentials=True,
)
```

---

## 🧪 Como Testar CORS

### Método 1: HTML Simples

```html
<!DOCTYPE html>
<html>
<body>
    <button onclick="testar()">Testar CORS</button>
    <pre id="resultado"></pre>

    <script>
        async function testar() {
            try {
                const response = await fetch('http://localhost:8000/api');
                const data = await response.json();
                document.getElementById('resultado').textContent = 
                    'SUCESSO!\n' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('resultado').textContent = 
                    'ERRO: ' + error.message;
            }
        }
    </script>
</body>
</html>
```

### Método 2: Console do Navegador

1. Abra http://localhost:8000/docs
2. Abra DevTools (F12)
3. No Console, execute:

```javascript
fetch('http://localhost:8000/api')
    .then(r => r.json())
    .then(data => console.log('Sucesso!', data))
    .catch(err => console.error('Erro CORS!', err));
```

### Método 3: curl (Não Testa CORS!)

```bash
curl http://localhost:8000/api
```

**Atenção:** curl **não** é bloqueado por CORS! Só navegadores são.

---

## 📚 Recursos Adicionais

### Documentação

- [FastAPI - CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN - CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [W3C CORS Spec](https://www.w3.org/TR/cors/)

### Ferramentas

- [Test CORS](https://www.test-cors.org/)
- Chrome DevTools Network Tab

---

## 
