# Scripts de Setup - Bloco 2

## 📁 Conteúdo

Este diretório contém scripts auxiliares para configurar o Git:

### **1. setup_git.sh / setup_git.bat**
Configura o Git pela primeira vez no seu computador (nome e email).

### **2. init_git_history.sh**
Inicializa o histórico Git nos exemplos (necessário após baixar o material).

---

## 🚀 Como Usar

### **Primeira Vez Usando Git? Configure-o:**

**Windows:**
```bash
./setup_git.bat
```

**Linux/Mac:**
```bash
chmod +x setup_git.sh
./setup_git.sh
```

---

### **Baixou o Material da Aula? Inicialize o Histórico:**

Este passo é necessário porque o Git não consegue ser enviado via ZIP.

**Linux/Mac:**
```bash
cd bloco2-git
chmod +x scripts/init_git_history.sh
./scripts/init_git_history.sh
```

**Windows (PowerShell):**
```powershell
cd bloco2-git
bash scripts/init_git_history.sh
```

**Ou manualmente (qualquer OS):**
```bash
# Para exemplo-inicial
cd exemplo-inicial
git init -b main
git config user.email "seu@email.com"
git config user.name "Seu Nome"
git add main.py
git commit -m "feat: Versão inicial"

# Para exemplo-rollback
cd ../exemplo-rollback
git init -b main
git config user.email "seu@email.com"
git config user.name "Seu Nome"
git add main.py
git commit -m "feat: Versão com bug"
```

---

## ⚠️ Importante

Estes scripts são apenas auxiliares. O conteúdo principal da aula está em:
- `exemplo-inicial/`: API estável
- `exemplo-rollback/`: Cenário de rollback

---

## 🆘 Problemas Comuns

### "git: command not found"
Instale o Git:
- **Windows**: https://git-scm.com/downloads
- **Linux**: `sudo apt-get install git`
- **Mac**: `brew install git`

### "Permission denied" (Linux/Mac)
Torne o script executável:
```bash
chmod +x setup_git.sh
```

### Git já configurado
Os scripts detectam se o Git já está configurado e permitem reconfigurar se necessário.
