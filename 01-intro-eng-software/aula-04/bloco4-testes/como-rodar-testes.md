# Como Rodar Testes com Pytest

## 📋 Pré-requisitos

### Instalar pytest
```bash
pip install pytest fastapi httpx
```

## 🚀 Comandos Básicos

### 1. Rodar todos os testes
```bash
pytest
```

### 2. Rodar com verbosidade (mostra detalhes)
```bash
pytest -v
```

### 3. Rodar um arquivo específico
```bash
pytest test_main.py
```

### 4. Rodar um teste específico
```bash
pytest test_main.py::test_fraude_detectada_valor_alto
```

### 5. Mostrar print() nos testes (útil para debug)
```bash
pytest -s
```

### 6. Parar no primeiro erro
```bash
pytest -x
```

### 7. Mostrar resumo de testes
```bash
pytest --tb=short
```

## 🎯 Demonstração Prática: Detectar Regressão

### Passo 1: Testar versão CORRETA
```bash
cd 3-exemplo-regressao

# Copiar versão correta
cp main_correto.py main.py

# Rodar testes
pytest -v
```

**Resultado esperado:** ✅✅✅ Todos os testes PASSAM

### Passo 2: Testar versão QUEBRADA
```bash
# Copiar versão quebrada (threshold mudou de 10k para 15k)
cp main_quebrado.py main.py

# Rodar testes
pytest -v
```

**Resultado esperado:** ❌❌ Testes FALHAM detectando a regressão!

**Mensagem de erro:**
```
FAILED test_main.py::test_fraude_detectada_valor_alto
AssertionError: REGRESSÃO DETECTADA! R$ 15.000 deveria ser fraude...
```

### Passo 3: Entender o que aconteceu
O teste `test_fraude_detectada_valor_alto` espera que R$ 15.000 seja fraude (threshold > 10k).

Na versão quebrada, o threshold foi aumentado para R$ 15k, então R$ 15.000 NÃO é mais considerado fraude.

O teste detectou essa mudança e BLOQUEOU o deploy!

## 📊 Interpretando os Resultados

### ✅ Teste passou
```
test_main.py::test_fraude_detectada_valor_alto PASSED
```

### ❌ Teste falhou
```
test_main.py::test_fraude_detectada_valor_alto FAILED
```

### Estatísticas
```
====== 3 passed in 0.52s ======  ✅ Tudo OK!
====== 2 failed, 1 passed ======  ❌ Tem problema!
```

## 🛡️ O Campo de Força em Ação

### Como funciona:
1. Desenvolvedor faz mudança no código
2. Roda `pytest` localmente
3. Testes FALHAM se a mudança viola regras de negócio
4. Deploy é BLOQUEADO até corrigir

### Em produção (CI/CD):
```
GitHub Actions → roda pytest → Se falhar → PR bloqueado ❌
                             → Se passar → PR aprovado ✅
```

## 💡 Boas Práticas

### ✅ O que fazer:
- Rodar testes ANTES de commitar
- Escrever testes para todas as regras de negócio
- Usar nomes descritivos nos testes
- Seguir padrão AAA (Arrange, Act, Assert)

### ❌ O que NÃO fazer:
- Commitar código sem rodar testes
- Deletar testes que estão falhando
- Fazer deploy se testes falharem
- Ignorar mensagens de erro dos testes

## 🔧 Troubleshooting

### Erro: "No module named 'pytest'"
```bash
pip install pytest
```

### Erro: "No module named 'fastapi'"
```bash
pip install fastapi httpx
```

### Erro: "No tests ran"
Verifique se:
- Arquivos começam com `test_`
- Funções começam com `test_`
- Você está no diretório correto

### Testes não encontram o módulo `main`
```bash
# Certifique-se de estar no diretório correto
cd 2-com-testes
pytest -v
```

## 📚 Recursos Adicionais

- Documentação oficial: https://docs.pytest.org
- FastAPI Testing: https://fastapi.tiangolo.com/tutorial/testing/
