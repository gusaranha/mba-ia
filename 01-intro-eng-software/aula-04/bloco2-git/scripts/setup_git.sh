#!/bin/bash

# Script de Setup do Git - Linux/Mac
# Configura Git pela primeira vez no seu computador

echo "========================================="
echo "   Setup do Git - Aula 4"
echo "========================================="
echo ""

# Verificar se Git está instalado
if ! command -v git &> /dev/null
then
    echo "❌ Git não está instalado!"
    echo ""
    echo "Por favor, instale o Git primeiro:"
    echo "  - Ubuntu/Debian: sudo apt-get install git"
    echo "  - MacOS: brew install git"
    echo "  - Ou baixe em: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git encontrado: $(git --version)"
echo ""

# Verificar se já está configurado
if git config --global user.name &> /dev/null && git config --global user.email &> /dev/null
then
    echo "✅ Git já está configurado:"
    echo "   Nome: $(git config --global user.name)"
    echo "   Email: $(git config --global user.email)"
    echo ""
    read -p "Deseja reconfigurar? (s/N): " reconfig
    if [[ ! $reconfig =~ ^[Ss]$ ]]
    then
        echo "Setup concluído!"
        exit 0
    fi
    echo ""
fi

# Configurar nome
echo "📝 Configurando seu perfil Git..."
echo ""
read -p "Digite seu nome completo: " nome
git config --global user.name "$nome"

# Configurar email
read -p "Digite seu email: " email
git config --global user.email "$email"

# Configurações adicionais recomendadas
echo ""
echo "⚙️  Aplicando configurações recomendadas..."
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global pull.rebase false

echo ""
echo "========================================="
echo "✅ Setup concluído com sucesso!"
echo "========================================="
echo ""
echo "Suas configurações:"
echo "  Nome: $(git config --global user.name)"
echo "  Email: $(git config --global user.email)"
echo ""
echo "Próximos passos:"
echo "  1. Navegue até exemplo-inicial/"
echo "  2. Execute: git log --oneline"
echo "  3. Explore o histórico de commits!"
echo ""
