# ✅ Exemplo 3: COM CORS

## 🎯 Objetivo

Mostrar como configurar CORS para permitir que frontends (navegadores) consumam a API.

---

## 🌐 O Que é CORS?

**CORS** = Cross-Origin Resource Sharing

### O Problema

```
Frontend: http://meu-site.com
    ↓ tenta chamar
API: http://localhost:8000
    ↓
❌ Navegador BLOQUEIA por segurança!
```

### A Solução

```python
# Configurar CORS no FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Quais sites podem acessar
    allow_methods=["*"],  # Quais métodos (GET, POST, etc)
    allow_headers=["*"]   # Quais headers
)
```

---

## 🚀 Como Rodar

### 1. Instalar Dependências

```bash
pip install fastapi uvicorn python-dotenv
```

### 2. Criar Arquivo .env

```bash
# Na pasta 3-com-cors/
cp .env.example .env
```

### 3. Verificar .env

O arquivo `.env` deve conter:

```env
CORS_ORIGINS=*
```

**Atenção**: `*` permite QUALQUER origem (ok para desenvolvimento)

### 4. Rodar a API

```bash
uvicorn main:app --reload
```

### 5. Testar CORS com HTML

Abra o arquivo `test_cors.html` no navegador:

```bash
# Windows
start test_cors.html

# macOS
open test_cors.html

# Linux
xdg-open test_cors.html
```

---

## 🧪 Testando CORS

### Teste 1: Via HTML (Recomendado)

1. Abra `test_cors.html` no navegador
2. Clique em "✅ Testar Health Check"
3. Veja a resposta!

**Resultado Esperado:**

```
✅ SUCESSO! CORS está funcionando!

Health Check:
{
  "status": "healthy",
  "timestamp": "...",
  "cors_enabled": true
}
```

### Teste 2: Via Swagger

- Acesse: http://localhost:8000/docs
- Funciona normalmente (Swagger roda no mesmo domínio)

### Teste 3: Via curl

```bash
curl http://localhost:8000/health
```

**Nota**: curl NÃO é bloqueado por CORS (só navegadores são)

---

## ⚙️ Configuração de CORS

### Desenvolvimento (Atual)

```env
# .env
CORS_ORIGINS=*
```

**Significado**: Qualquer site pode chamar sua API

✅ **Uso**: Desenvolvimento local  
❌ **NÃO use em produção!**

### Produção (Seguro)

```env
# .env
CORS_ORIGINS=https://meu-site.com,https://app.meu-site.com
```

**Significado**: Apenas esses sites podem chamar sua API

✅ **Uso**: Produção  
✅ **Seguro**: Controle total de acesso

---

## 📊 CORS: Dev vs Produção

| Aspecto        | Desenvolvimento         | Produção              |
| -------------- | ----------------------- | --------------------- |
| **Origens**    | `*` (qualquer)          | Específicas           |
| **Segurança**  | ⚠️ Baixa (mas ok local) | ✅ Alta                |
| **Facilidade** | ✅ Muito fácil           | ⚠️ Precisa configurar |
| **Uso**        | Testar rapidamente      | Deploy real           |

---

## 🔒 Segurança em Produção

### ❌ NUNCA Faça em Produção

```python
allow_origins=["*"]  # ❌ Qualquer site pode acessar!
```

### ✅ SEMPRE Faça em Produção

```python
allow_origins=[
    "https://meu-site.com",
    "https://app.meu-site.com"
]
```

### Como Configurar

**1. No .env de Produção:**

```env
CORS_ORIGINS=https://meu-site.com,https://app.meu-site.com
```

**2. O código já está preparado:**

```python
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
```

**3. Funciona!** ✅

---

## 🧪 Experimentos

### Experimento 1: Desabilitar CORS

**1. Comente o middleware no código:**

```python
# app.add_middleware(
#     CORSMiddleware,
#     ...
# )
```

**2. Reinicie a API**

**3. Abra `test_cors.html`**

**Resultado**: ❌ Erro "CORS policy"!

### Experimento 2: CORS Específico

**1. No .env:**

```env
CORS_ORIGINS=http://localhost:3000
```

**2. Abra `test_cors.html` de outro domínio**

**Resultado**: ❌ Bloqueado! (só localhost:3000 permitido)

---

## 💡 Quando Usar CORS?

### ✅ Precisa de CORS

- Frontend React/Vue/Angular consumindo API
- Website público chamando API
- Aplicação mobile web
- Qualquer app no navegador chamando API

### ❌ NÃO Precisa de CORS

- API só para backend (servidor para servidor)
- Testes via curl/Postman
- Scripts Python chamando API
- Swagger da própria API

---

## 🎓 Exercício

**Desafio**: Configure CORS para múltiplos domínios

**1. Edite .env:**

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**2. Verifique:**

```bash
curl http://localhost:8000/config
```

**3. Veja:**

```json
{
  "cors_origins": ["http://localhost:3000", "http://localhost:5173"]
}
```

---

## 📚 Recursos Adicionais

### Documentação

- [FastAPI - CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN - CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

### Artigos

- [CORS Explained](https://web.dev/cross-origin-resource-sharing/)

---

## ❓ Perguntas Frequentes

**P: Por que o Swagger funciona sem CORS?**  
R: Swagger roda no MESMO domínio da API (http://localhost:8000)

**P: curl funciona sem CORS?**  
R: Sim! CORS só afeta navegadores, não ferramentas de linha de comando.

**P: Devo usar "*" em produção?**  
R: ❌ NUNCA! Sempre especifique domínios permitidos.

**P: Como testar CORS sem frontend?**  
R: Use o `test_cors.html` fornecido!

**P: CORS resolve problemas de autenticação?**  
R: Não! CORS é sobre ONDE pode chamar, não QUEM pode chamar.

---

## ✅ Checklist Final

Antes de ir para produção, verifique:

- [ ] CORS_ORIGINS tem domínios específicos (não "*")
- [ ] .env está no .gitignore
- [ ] Testou com frontend real
- [ ] Verificou allow_credentials (se usa cookies)
- [ ] Documentou origens permitidas

---

**Parabéns!** Agora sua API pode ser consumida por frontends! 🎉

**Próximo**: Combine .env + CORS no seu projeto real!
