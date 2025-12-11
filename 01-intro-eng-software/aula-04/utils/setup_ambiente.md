# Setup do Ambiente - Aula 4

## 🎯 Objetivo
Configurar o ambiente de desenvolvimento para a Aula 4 de Controle de Qualidade.

## 📋 Checklist de Instalação

- [ ] Python 3.8+
- [ ] Git
- [ ] VS Code (recomendado)
- [ ] Conta no GitHub
- [ ] Dependências Python

---

## 1️⃣ Python

### Verificar se já está instalado
```bash
python --version
# ou
python3 --version
```

**Versão mínima:** 3.8

### Instalar Python

#### Windows
1. Baixe em: https://www.python.org/downloads/
2. **IMPORTANTE**: Marque "Add Python to PATH"
3. Execute o instalador
4. Verifique: `python --version`

#### macOS
```bash
# Usando Homebrew
brew install python3
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 2️⃣ Git

### Verificar se já está instalado
```bash
git --version
```

### Instalar Git

#### Windows
1. Baixe em: https://git-scm.com/download/win
2. Execute o instalador (configurações padrão)
3. Verifique: `git --version`

#### macOS
```bash
# Usando Homebrew
brew install git
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

### Configurar Git (Primeira vez)
```bash
# Seu nome
git config --global user.name "Seu Nome"

# Seu email
git config --global user.email "seu.email@example.com"

# Verificar configurações
git config --list
```

---

## 3️⃣ VS Code (Recomendado)

### Download
https://code.visualstudio.com/

### Extensões Recomendadas
- Python (Microsoft)
- Pylance
- GitLens
- Python Test Explorer

### Instalar extensões
1. Abra VS Code
2. Clique no ícone de extensões (Ctrl+Shift+X)
3. Busque e instale cada uma

---

## 4️⃣ GitHub

### Criar conta (se não tiver)
1. Acesse: https://github.com
2. Clique em "Sign up"
3. Siga os passos

### Configurar SSH (Opcional mas recomendado)

#### Gerar chave SSH
```bash
ssh-keygen -t ed25519 -C "seu.email@example.com"
# Pressione Enter 3 vezes (sem senha)
```

#### Adicionar ao GitHub
```bash
# Copiar chave pública
cat ~/.ssh/id_ed25519.pub
```

1. Acesse: https://github.com/settings/keys
2. Clique em "New SSH key"
3. Cole a chave copiada
4. Clique em "Add SSH key"

#### Testar conexão
```bash
ssh -T git@github.com
```

---

## 5️⃣ Clonar o Repositório

### Opção 1: HTTPS (mais simples)
```bash
git clone https://github.com/seu-usuario/aula4-controle-qualidade.git
cd aula4-controle-qualidade
```

### Opção 2: SSH (se configurou)
```bash
git clone git@github.com:seu-usuario/aula4-controle-qualidade.git
cd aula4-controle-qualidade
```

### Opção 3: Download ZIP (sem Git)
1. Acesse o repositório no GitHub
2. Clique em "Code" > "Download ZIP"
3. Descompacte
4. Abra a pasta no VS Code

---

## 6️⃣ Criar Ambiente Virtual (Recomendado)

### Por que usar?
Isola as dependências do projeto, evitando conflitos.

### Criar ambiente virtual
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### Ativar ambiente virtual

#### Windows (CMD)
```bash
venv\Scripts\activate
```

#### Windows (PowerShell)
```bash
venv\Scripts\Activate.ps1
```

#### macOS/Linux
```bash
source venv/bin/activate
```

### Verificar ativação
Você verá `(venv)` no início da linha de comando.

### Desativar (quando terminar)
```bash
deactivate
```

---

## 7️⃣ Instalar Dependências

### Com ambiente virtual ativado:
```bash
pip install -r requirements.txt
```

### Verificar instalação
```bash
# FastAPI
python -c "import fastapi; print(fastapi.__version__)"

# Pytest
pytest --version

# Uvicorn
uvicorn --version
```

---

## 8️⃣ Verificação Final

### Teste rápido - Rodar uma API
```bash
cd bloco3-debug-logs/2-com-logs
uvicorn main:app --reload
```

Acesse: http://localhost:8000/docs

Se abrir a documentação Swagger, está tudo OK! ✅

### Teste rápido - Rodar testes
```bash
cd bloco4-testes/2-com-testes
pytest -v
```

Se os testes passarem, está tudo OK! ✅

---

## 🆘 Problemas Comuns

### "python não é reconhecido como comando"
- **Windows**: Python não está no PATH
- **Solução**: Reinstale marcando "Add Python to PATH"

### "pip não é reconhecido como comando"
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

### "Permission denied" ao instalar pacotes
```bash
# Não use sudo!
# Use ambiente virtual ou:
pip install --user -r requirements.txt
```

### Porta 8000 já está em uso
```bash
# Use outra porta
uvicorn main:app --reload --port 8001
```

### Import error no pytest
```bash
# Certifique-se de estar no diretório correto
cd bloco4-testes/2-com-testes
pytest -v
```

---

## 📚 Comandos Úteis

### Ver versão do Python
```bash
python --version
```

### Ver pacotes instalados
```bash
pip list
```

### Atualizar pip
```bash
pip install --upgrade pip
```

### Instalar pacote específico
```bash
pip install fastapi
```

### Desinstalar pacote
```bash
pip uninstall fastapi
```

### Criar novo requirements.txt
```bash
pip freeze > requirements.txt
```

---

## ✅ Checklist Final

Antes da aula, verifique:

- [ ] Python instalado e funcionando
- [ ] Git instalado e configurado
- [ ] VS Code instalado (opcional)
- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] API de teste rodando
- [ ] Pytest funcionando

---

## 💡 Dicas

### Durante a aula:
1. **Mantenha o ambiente virtual ativado**
2. **Tenha duas janelas de terminal abertas**: uma para API, outra para comandos
3. **Use VS Code**: facilita muito o desenvolvimento
4. **Não tenha medo de errar**: é assim que se aprende!

### Organização:
```
Terminal 1: Rodar API
uvicorn main:app --reload

Terminal 2: Comandos Git, Pytest, etc.
git log
pytest -v
```

---

## 🎓 Pronto para a Aula!

Se todos os itens do checklist estão ✅, você está pronto!

Qualquer problema, consulte: `utils/troubleshooting.md`

**Boa aula! 🚀**
