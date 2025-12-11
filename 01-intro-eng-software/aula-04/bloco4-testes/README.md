# Bloco 4: Testes Automatizados

## 🎯 Objetivo
Aprender a criar testes automatizados que garantem a qualidade do código e impedem regressões.

## 📂 Estrutura

### 1-sem-testes/
API sem testes automatizados (arriscado!)

### 2-com-testes/
API com testes automatizados usando pytest

### 3-exemplo-regressao/
Demonstração prática de como testes detectam regressões

## 🚀 Como Usar

### Instalar pytest
```bash
pip install pytest
```

### Rodar testes
```bash
cd 2-com-testes
pytest -v
```

### Testar detecção de regressão
```bash
cd 3-exemplo-regressao

# Versão correta (testes passam)
cp main_correto.py main.py
pytest -v

# Versão quebrada (testes falham)
cp main_quebrado.py main.py
pytest -v
```

## 💡 Conceitos Importantes

### O que são testes automatizados?
Robôs que validam se o código funciona corretamente

### Por que testar?
- Detectar bugs antes de produção
- Evitar regressões (quebrar funcionalidades antigas)
- Documentar o comportamento esperado

### O Campo de Força
Testes são como um escudo protetor: qualquer mudança que viole as regras de negócio é bloqueada automaticamente.
