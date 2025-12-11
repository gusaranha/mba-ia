Roteiro Simplificado: Git + GitHub + VS Code
Passo 1: Instalar o Git
Windows

Acesse: https://git-scm.com/download/win
Execute o instalador baixado
Durante a instalação:

Escolha o editor: selecione "Use Visual Studio Code as Git's default editor"
Demais opções: deixe padrão


Clique em "Install" e depois "Finish"

macOS
bash# Via Homebrew:
brew install git
Linux (Ubuntu/Debian)
bashsudo apt update
sudo apt install git
Verificar Instalação
bashgit --version

Passo 2: Configurar o Git
No terminal, execute:
bashgit config --global user.name "Seu Nome Completo"
git config --global user.email "seu.email@exemplo.com"

Passo 3: Criar Conta no GitHub

Acesse: https://github.com/
Clique em "Sign up"
Preencha: email, senha e username
Verifique seu email (clique no link de confirmação)


Passo 4: Conectar VS Code ao GitHub
4.1 Instalar Extensão

Abra o VS Code
Clique em Extensions (ícone de quadrados no menu lateral) ou Ctrl+Shift+X
Busque: "GitHub Pull Requests and Issues"
Clique em Install

4.2 Fazer Login no GitHub

No VS Code, clique no ícone de conta (pessoa) no canto inferior esquerdo
Clique em "Sign in with GitHub"
Uma página do navegador abrirá
Clique em Authorize Visual-Studio-Code
Pronto! VS Code está conectado


Passo 5: Testar Tudo Funcionando
5.1 Criar Repositório no GitHub

No GitHub, clique em + (canto superior direito) > New repository
Nome: teste-vscode
Marque: Add a README file
Clique em Create repository

5.2 Clonar no VS Code

No GitHub, clique no botão verde Code
Copie a URL HTTPS (não SSH!)
No VS Code: Ctrl+Shift+P > digite "Git: Clone"
Cole a URL
Escolha uma pasta
Clique em "Open" quando aparecer

5.3 Fazer uma Mudança

Abra o arquivo README.md
Adicione: Testando Git + VS Code!
Salve (Ctrl+S)
Clique no ícone Source Control (menu lateral) ou Ctrl+Shift+G
Clique no + ao lado do arquivo
Digite a mensagem: "Meu primeiro commit"
Clique em ✓ Commit
Clique em Sync Changes

Na primeira vez, uma janela pedirá para fazer login - autorize no navegador que abrir.

Volte ao GitHub e atualize - sua mudança está lá! ✅


✅ Checklist

 Git instalado
 Git configurado (nome e email)
 Conta GitHub criada
 VS Code conectado ao GitHub
 Repositório clonado e modificado com sucesso


Comandos Básicos (Pode Usar pelo Terminal do VS Code)
bashgit status          # Ver arquivos modificados
git add .           # Adicionar tudo
git commit -m "msg" # Salvar versão
git push            # Enviar para GitHub
git pull            # Baixar do GitHub