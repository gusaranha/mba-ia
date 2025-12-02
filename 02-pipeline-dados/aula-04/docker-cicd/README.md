# 🏦 Calculadora de Score de Crédito


## O que faz

Calcula score de crédito (0-100) baseado em:
- 💰 Renda
- 👤 Idade  
- 💳 Dívidas

---

## 📁 Estrutura (SUPER SIMPLES!)

```
docker-cicd-demo/
├── calculadora.py          # Lógica principal (30 linhas)
├── validador.py            # Valida dados com Pandera
├── test_calculadora.py     # Testes com pytest
├── clientes.csv            # Dados exemplo
├── requirements.txt        # 3 bibliotecas
├── Dockerfile              # Container (15 linhas)
└── .github/workflows/
    └── testes.yml          # CI/CD (30 linhas)
```

**Total:** ~100 linhas de código!

---

## 🚀 Como Usar Localmente

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar calculadora
```bash
python calculadora.py
```

**Output:**
```
🏦 Calculadora de Score de Crédito
========================================

Renda: R$ 6000.00
Idade: 35 anos
Dívidas: R$ 2000.00
Score: 85 (Alto)

Renda: R$ 2000.00
Idade: 22 anos
Dívidas: R$ 8000.00
Score: 20 (Baixo)
```

### 3. Validar dados
```bash
python validador.py
```

**Output:**
```
✅ Testando validação...
✅ Dados válidos passaram!
❌ Dados inválidos rejeitados (correto!): Idade mínima: 18 anos
```

### 4. Rodar testes
```bash
pytest test_calculadora.py -v
```

**Output:**
```
test_calculadora.py::test_score_alto PASSED        [25%]
test_calculadora.py::test_score_baixo PASSED       [50%]
test_calculadora.py::test_score_medio PASSED       [75%]
test_calculadora.py::test_score_dentro_limites PASSED [100%]

✅ 4 passed
```

---

## 🐳 Docker 

### O que é Docker?
**Empacota código + dependências em um "container"**

Problema: "Funciona na minha máquina" ≠ funciona em outras  
Solução: Container com TUDO dentro

### Ver Dockerfile
```bash
cat Dockerfile
```

**O que tem:**
```dockerfile
FROM python:3.11-slim      # 1. Imagem base
WORKDIR /app               # 2. Pasta
COPY requirements.txt .    # 3. Copiar deps
RUN pip install -r ...     # 4. Instalar
COPY . .                   # 5. Copiar código
CMD ["python", "calculadora.py"]  # 6. Rodar
```

### Construir container
```bash
docker build -t calculadora-score .
```

**O que acontece:**
- Baixa Python 3.11
- Instala pandas, pandera, pytest
- Copia todo código
- Fica pronto!

### Rodar container
```bash
docker run calculadora-score
```

**Resultado:** Mesma saída da calculadora, mas rodando DENTRO do container!

### Rodar testes no container
```bash
docker run calculadora-score pytest test_calculadora.py -v
```

**Resultado:** Testes rodam dentro do container (ambiente isolado)

---

##  CI/CD

### O que é CI/CD?
**Testes automáticos em cada commit**

Cenário SEM CI/CD:
```
Programador: Altera código
Programador: "Acho que tá funcionando..." 🤔
Programador: Faz commit
Sistema: Quebra! 💥
```

Cenário COM CI/CD:
```
Programador: Altera código
GitHub: Roda testes AUTOMATICAMENTE
GitHub: ❌ "Teste falhou! Validação de idade quebrou"
Programador: Corrige ANTES de quebrar produção ✅
```

### Ver workflow
```bash
cat .github/workflows/testes.yml
```

**O que tem:**
```yaml
steps:
  - Baixar código
  - Instalar Python
  - Instalar dependências
  - Validar dados (Pandera!)  ← AUTOMÁTICO!
  - Rodar testes (pytest!)    ← AUTOMÁTICO!
```

### Como funciona?

1. **Você faz commit**
2. **GitHub detecta automaticamente**
3. **Roda todos os steps**
4. **Se passar:** ✅ Pode fazer merge
5. **Se falhar:** ❌ Bloqueia merge

### Ver resultados

Acessar: `github.com/[seu-repo]/actions`

**Exemplo de sucesso:**
```
✅ Baixar código           2s
✅ Instalar Python         3s
✅ Instalar dependências  12s
✅ Validar dados           1s
✅ Rodar testes            3s

Total: 21s - PASSOU!
```

**Exemplo de falha:**
```
✅ Baixar código           2s
✅ Instalar Python         3s
✅ Instalar dependências  12s
❌ Validar dados           1s
   Erro: Idade mínima: 18 anos
   
❌ FALHOU - Commit bloqueado
```

---

## Conceitos Demonstrados

### Docker
- ✅ Containerização
- ✅ Isolamento de ambiente
- ✅ Portabilidade ("funciona igual em todos lugares")
- ✅ Dockerfile (receita do container)

### CI/CD
- ✅ Testes automáticos
- ✅ Validação de dados (Pandera)
- ✅ Testes unitários (pytest)
- ✅ GitHub Actions
- ✅ Integração contínua



---
