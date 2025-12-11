# Troubleshooting - Soluções para Problemas Comuns

## 🎯 Guia de Resolução de Problemas

Este documento contém soluções para os problemas mais comuns encontrados durante a Aula 4.

---

## 🐍 Problemas com Python

### ❌ "python não é reconhecido como comando"

**Problema:** Python não está no PATH do sistema.

**Soluções:**

#### Windows
1. Reinstale o Python marcando "Add Python to PATH"
2. Ou adicione manualmente:
   - Busque por "Variáveis de ambiente" no Windows
   - Edite PATH
   - Adicione: `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python3XX`

#### macOS/Linux
```bash
# Adicione ao ~/.bashrc ou ~/.zshrc
export PATH="/usr/local/bin:$PATH"

# Recarregue
source ~/.bashrc  # ou ~/.zshrc
```

**Alternativa temporária:**
```bash
# Use python3 em vez de python
python3 --version
python3 -m pip install -r requirements.txt
```

---

### ❌ "pip não é reconhecido como comando"

**Solução:**
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

---

### ❌ "Permission denied" ao instalar pacotes

**Problema:** Tentando instalar sem permissões adequadas.

**❌ NÃO FAÇA:**
```bash
sudo pip install ...  # Nunca use sudo!
```

**✅ SOLUÇÕES:**

1. **Use ambiente virtual** (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Instale localmente**:
```bash
pip install --user -r requirements.txt
```

---

### ❌ Versão antiga do Python

**Verificar versão:**
```bash
python --version
```

**Mínimo necessário:** Python 3.8

**Solução:** Instale uma versão mais recente:
- Windows/macOS: https://www.python.org/downloads/
- Linux: Use o gerenciador de pacotes

---

## 🔧 Problemas com Dependências

### ❌ "No module named 'fastapi'"

**Problema:** FastAPI não está instalado.

**Solução:**
```bash
pip install fastapi uvicorn
```

---

### ❌ "No module named 'pytest'"

**Solução:**
```bash
pip install pytest
```

---

### ❌ "No module named 'httpx'"

**Problema:** Necessário para TestClient do FastAPI.

**Solução:**
```bash
pip install httpx
```

---

### ❌ Erro ao instalar dependências

**Problema:** requirements.txt com problemas.

**Solução:** Instale manualmente:
```bash
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pydantic==2.5.0
pip install pytest==7.4.3
pip install httpx==0.25.2
pip install python-json-logger==2.0.7
```

---

## 🚀 Problemas com FastAPI/Uvicorn

### ❌ "Address already in use" (Porta 8000 ocupada)

**Problema:** Já existe uma aplicação rodando na porta 8000.

**Soluções:**

1. **Use outra porta:**
```bash
uvicorn main:app --reload --port 8001
```

2. **Mate o processo anterior:**

#### Windows
```bash
# Encontre o processo
netstat -ano | findstr :8000

# Mate o processo (use o PID encontrado)
taskkill /PID <numero_do_pid> /F
```

#### macOS/Linux
```bash
# Encontre e mate o processo
lsof -ti:8000 | xargs kill -9
```

---

### ❌ "ModuleNotFoundError: No module named 'main'"

**Problema:** Uvicorn não encontra o arquivo main.py

**Soluções:**

1. **Verifique se está no diretório correto:**
```bash
# Deve estar no mesmo diretório do main.py
ls main.py  # Deve listar o arquivo

# Se não estiver, navegue até lá
cd bloco3-debug-logs/2-com-logs
```

2. **Verifique o nome do arquivo:**
```bash
# Se o arquivo se chama app.py em vez de main.py
uvicorn app:app --reload
```

---

### ❌ "ERROR: [Errno 98] Address already in use"

**Solução rápida:**
```bash
# Reinicie com outra porta
uvicorn main:app --reload --port 8001
```

---

## 🧪 Problemas com Pytest

### ❌ "No tests ran"

**Problema:** Pytest não encontrou os testes.

**Causas e soluções:**

1. **Arquivo não começa com test_:**
```bash
# ❌ Errado
arquivo.py

# ✅ Correto
test_arquivo.py
```

2. **Função não começa com test_:**
```python
# ❌ Errado
def verificar_api():
    pass

# ✅ Correto
def test_verificar_api():
    pass
```

3. **Não está no diretório correto:**
```bash
cd bloco4-testes/2-com-testes
pytest -v
```

---

### ❌ "ModuleNotFoundError: No module named 'main'"

**Problema:** Pytest não encontra o módulo main.

**Solução:**
```bash
# Certifique-se de estar no diretório correto
cd bloco4-testes/2-com-testes

# Deve haver main.py e test_main.py no mesmo diretório
ls main.py test_main.py
```

---

### ❌ Testes falham mas a API funciona

**Problema:** TestClient não está configurado corretamente.

**Verifique o código:**
```python
# test_main.py deve ter:
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_exemplo():
    response = client.get("/")
    assert response.status_code == 200
```

---

## 🔀 Problemas com Git

### ❌ "git não é reconhecido como comando"

**Problema:** Git não está instalado ou não está no PATH.

**Solução:** Instale o Git:
- Windows: https://git-scm.com/download/win
- macOS: `brew install git`
- Linux: `sudo apt install git`

---

### ❌ "Permission denied (publickey)"

**Problema:** Tentando usar SSH sem configurar chave.

**Soluções:**

1. **Use HTTPS em vez de SSH:**
```bash
# Em vez de:
git clone git@github.com:usuario/repo.git

# Use:
git clone https://github.com/usuario/repo.git
```

2. **Configure chave SSH:**
```bash
ssh-keygen -t ed25519 -C "seu.email@example.com"
cat ~/.ssh/id_ed25519.pub
# Adicione em: https://github.com/settings/keys
```

---

### ❌ "fatal: not a git repository"

**Problema:** Não está em um diretório Git.

**Solução:**
```bash
# Navegue até o repositório
cd aula4-controle-qualidade

# Ou inicialize um novo repo
git init
```

---

### ❌ "Your local changes would be overwritten"

**Problema:** Há mudanças locais não commitadas.

**Soluções:**

1. **Commitar mudanças:**
```bash
git add .
git commit -m "Salvar mudanças locais"
```

2. **Descartar mudanças:**
```bash
git stash  # Salva temporariamente
# ou
git reset --hard  # ⚠️ Perde as mudanças!
```

---

## 💻 Problemas com VS Code

### ❌ Python não é detectado no VS Code

**Solução:**

1. Instale a extensão Python (Microsoft)
2. Pressione `Ctrl+Shift+P`
3. Digite: "Python: Select Interpreter"
4. Selecione o Python correto (ou do ambiente virtual)

---

### ❌ Terminal não abre no VS Code

**Solução:**
- Pressione: `Ctrl + '` (Windows/Linux)
- Pressione: `Cmd + '` (macOS)
- Ou: Menu "Terminal" > "New Terminal"

---

### ❌ Debugger não funciona

**Solução:**

1. Crie `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```

---

## 🌐 Problemas de Rede

### ❌ "Connection timeout" ao clonar repositório

**Soluções:**

1. **Verifique sua conexão com internet**

2. **Baixe o ZIP em vez de clonar:**
   - Acesse o repo no GitHub
   - Clique em "Code" > "Download ZIP"

3. **Use proxy (se necessário):**
```bash
git config --global http.proxy http://proxy.example.com:8080
```

---

### ❌ API não abre no navegador

**Problema:** localhost:8000 não responde.

**Verificações:**

1. **API está rodando?**
```bash
# Terminal deve mostrar:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

2. **Porta correta?**
```bash
# Se rodou em outra porta:
uvicorn main:app --reload --port 8001
# Acesse: http://localhost:8001
```

3. **Firewall bloqueando?**
- Windows: Permita o Python no firewall
- macOS: Permita nas preferências de segurança

---

## 🖥️ Problemas Específicos do Sistema Operacional

### Windows

#### PowerShell não executa scripts
```bash
# Execute como Administrador:
Set-ExecutionPolicy RemoteSigned
```

#### Backslash vs Forward slash
```bash
# Windows aceita ambos, mas prefira:
cd bloco2-git\exemplo-inicial  # Windows style
# ou
cd bloco2-git/exemplo-inicial  # Unix style (também funciona)
```

---

### macOS

#### "Developer tools not installed"
```bash
xcode-select --install
```

#### Python aponta para versão 2.7
```bash
# Use python3 explicitamente
python3 --version
python3 -m pip install -r requirements.txt
```

---

### Linux

#### Problemas com permissões
```bash
# Não use sudo pip!
# Use ambiente virtual ou --user
pip install --user -r requirements.txt
```

---

## 📱 Problemas Durante a Aula

### ❌ Não consigo acompanhar a demonstração

**Soluções:**
1. **Não tente copiar linha por linha** - foque em entender o conceito
2. **Use o código pronto** - está no repositório
3. **Pergunte no chat** - outros podem ter a mesma dúvida
4. **Revise depois** - o material fica disponível

---

### ❌ Código do instrutor funciona, mas o meu não

**Checklist:**
- [ ] Mesmo diretório?
- [ ] Mesma versão das dependências?
- [ ] Código igual? (copie e cole se necessário)
- [ ] Ambiente virtual ativado?
- [ ] Porta disponível?

---

## 🆘 Última Solução: Começar do Zero

Se nada funcionar, recomeçe:

```bash
# 1. Remova o ambiente virtual
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# 2. Recrie
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# 3. Reinstale
pip install --upgrade pip
pip install -r requirements.txt

# 4. Teste
pytest --version
uvicorn --version
```

---

## 📞 Canais de Suporte

### Durante a aula:
- 🙋 Levante a mão virtual
- 💬 Pergunte no chat
- 📧 Chame o instrutor

### Após a aula:
- 📖 Consulte a documentação oficial
- 🐛 Abra uma Issue no GitHub
- 📧 Envie email para o instrutor

---

## 🔍 Comandos de Diagnóstico

Use estes comandos para diagnosticar problemas:

```bash
# Verificar versões
python --version
git --version
pip --version
pytest --version

# Verificar instalação
python -c "import fastapi; print('FastAPI OK')"
python -c "import pytest; print('Pytest OK')"

# Listar pacotes instalados
pip list

# Verificar se porta está ocupada (Linux/Mac)
lsof -i :8000

# Verificar se porta está ocupada (Windows)
netstat -ano | findstr :8000

# Testar conectividade
ping github.com
```

---

## ✅ Checklist de Verificação

Se algo não funciona, verifique:

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado e ativado (`(venv)` aparece no terminal)
- [ ] Dependências instaladas (`pip list` mostra fastapi, pytest, etc.)
- [ ] No diretório correto (`ls` mostra main.py)
- [ ] Nenhum processo ocupando a porta 8000
- [ ] Internet funcionando (se precisar baixar algo)

---

## 💡 Dicas Gerais

1. **Leia as mensagens de erro com atenção** - elas geralmente dizem o problema
2. **Google é seu amigo** - copie a mensagem de erro e busque
3. **Não tenha vergonha de perguntar** - todos passam por isso
4. **Documente sua solução** - pode ser útil depois
5. **Reinicie quando estiver muito perdido** - às vezes é mais rápido

---

**Problema não está aqui? Pergunte no chat ou abra uma Issue! 🚀**
