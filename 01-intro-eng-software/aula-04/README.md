# Aula 4 - Controle de Qualidade: Git, Debug e Testes

## 🎯 Objetivo da Aula
Aprender os três pilares fundamentais para garantir a qualidade e confiabilidade de sistemas em produção:
- **Git**: Governança e rastreabilidade
- **Debug/Logs**: Diagnóstico e observabilidade
- **Testes**: Validação e garantia

## 📋 Pré-requisitos

### Software necessário:
- Python 3.8+
- Git
- VS Code (recomendado)
- Conta no GitHub

### Conhecimentos:
- Aula 3 (FastAPI e Pydantic)
- Python básico

## 🚀 Setup Inicial

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/aula4-controle-qualidade.git
cd aula4-controle-qualidade
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Verifique a instalação
```bash
python --version
git --version
pytest --version
```

## 📂 Estrutura do Repositório

```
aula4-controle-qualidade/
│
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências do projeto
├── .gitignore                        # Arquivos ignorados pelo Git
│
├── bloco2-git/                       # 🔷 Git - Governança
│   ├── README.md
│   ├── exemplo-inicial/              # API com histórico Git
│   ├── exemplo-rollback/             # Demonstração de rollback
│   └── scripts/                      # Scripts de setup
│
├── bloco3-debug-logs/                # 🔍 Debug e Logs
│   ├── README.md
│   ├── 1-sem-logs/                   # API sem logs
│   ├── 2-com-logs/                   # API com logs estruturados
│   ├── 3-exemplo-bug/                # Exemplo de debugging
│   └── como-debugar.md
│
├── bloco4-testes/                    # ✅ Testes Automatizados
│   ├── README.md
│   ├── 1-sem-testes/                 # API sem testes
│   ├── 2-com-testes/                 # API com testes
│   ├── 3-exemplo-regressao/          # Detectando regressões
│   └── como-rodar-testes.md
│
├── bloco5-projeto/                   # 🎓 Projeto Avaliativo
│   ├── README.md
│   ├── template/                     # Template inicial
│   └── exemplos/                     # Exemplos completos
│
└── utils/                            # 🛠️ Utilitários
    ├── setup_ambiente.md
    └── troubleshooting.md
```

## 📚 Conteúdo da Aula

### Bloco 1: Introdução (15min)
- O custo do risco em produção
- Conceito "Shift Left"
- Os três pilares de controle

### Bloco 2: Git - Governança e Rastreabilidade (45min)
- **Conceitos**: Git vs GitHub, recuperação de desastre
- **Comandos**: `git log`, `git revert`, `git blame`
- **Demonstração**: Rollback em produção
- **Governança**: Pull Requests

📁 Material: `bloco2-git/`

### Bloco 3: Debug e Observabilidade (40min)
- **Fase 1**: Debugger interativo (desenvolvimento)
- **Fase 2**: Logs estruturados (produção)
- **Demonstração**: Encontrar e corrigir bugs
- **JSON Logs**: Logs indexáveis e alertas automáticos

📁 Material: `bloco3-debug-logs/`

### Bloco 4: Testes Automatizados (50min)
- **Conceitos**: Regressão e "campo de força"
- **Estrutura**: Padrão AAA (Arrange, Act, Assert)
- **Pytest**: Testes automatizados
- **Demonstração**: Detectar regressão em produção

📁 Material: `bloco4-testes/`

### Bloco 5: Projeto Avaliativo (35min)
- Especificação do projeto final
- Template inicial fornecido
- Exemplos de referência
- Critérios de avaliação

📁 Material: `bloco5-projeto/`

## ⏱️ Cronograma

| Bloco | Tempo | Tipo |
|-------|-------|------|
| Setup Pré-Aula | 5min | Preparação |
| Bloco 1 - Introdução | 15min | Conceitual |
| Bloco 2 - Git | 45min | Demo + Conceitos |
| **Break** | 15min | - |
| Bloco 3 - Debug/Logs | 40min | Demo + Prática |
| **Break** | 15min | - |
| Bloco 4 - Testes | 50min | Demo + Prática |
| **Break** | 15min | - |
| Bloco 5 - Projeto | 35min | Especificação |
| **TOTAL** | **4h30** | - |

## 🎓 Projeto Avaliativo

### Objetivo
Construir uma API de lógica de negócio aplicando todos os pilares da aula.

### Requisitos Obrigatórios
- ✅ Repositório GitHub público
- ✅ README.md completo
- ✅ API FastAPI funcionando
- ✅ Validação com Pydantic
- ✅ Testes com Pytest (mínimo 2 testes)
- ✅ Histórico Git claro

### Prazo
**22/11/2025 às 23h59**

### Material
📁 `bloco5-projeto/` - Template e exemplos

## 🛠️ Comandos Rápidos

### Rodar uma API
```bash
cd bloco3-debug-logs/2-com-logs
uvicorn main:app --reload
```

### Rodar testes
```bash
cd bloco4-testes/2-com-testes
pytest -v
```

### Ver histórico Git
```bash
cd bloco2-git/exemplo-inicial
git log --oneline
```

## 📖 Recursos Adicionais

### Documentação
- [Git Documentation](https://git-scm.com/doc)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

### Guias Internos
- `utils/setup_ambiente.md` - Configuração do ambiente
- `utils/troubleshooting.md` - Solução de problemas comuns
- `bloco3-debug-logs/como-debugar.md` - Guia de debugging
- `bloco4-testes/como-rodar-testes.md` - Guia de testes

## 🆘 Precisa de Ajuda?

### Problemas comuns
Consulte `utils/troubleshooting.md`

### Durante a aula
- Levante a mão virtualmente
- Use o chat para perguntas
- Peça ajuda ao instrutor

### Após a aula
- Abra uma Issue no GitHub
- Envie email para o instrutor
- Consulte a documentação oficial

## 📝 Conceitos-Chave

### Git
> Sistema de controle de versão que mantém histórico completo do código, permitindo rastreabilidade e recuperação de desastres.

### Logs Estruturados
> Logs em formato JSON que podem ser indexados, pesquisados e usados para alertas automáticos em produção.

### Testes Automatizados
> Robôs que validam se o código funciona corretamente, criando um "campo de força" que impede regressões.

### Regressão
> Quando uma nova feature quebra uma funcionalidade antiga que estava funcionando.

### Shift Left
> Detectar e corrigir erros o mais cedo possível no ciclo de desenvolvimento, reduzindo custos exponencialmente.

## 🎯 Objetivos de Aprendizagem

Ao final desta aula, você será capaz de:

1. ✅ Usar Git para rastreabilidade e rollback
2. ✅ Criar logs estruturados para observabilidade
3. ✅ Escrever testes automatizados com Pytest
4. ✅ Detectar e prevenir regressões
5. ✅ Aplicar governança de código via Pull Requests
6. ✅ Construir APIs com qualidade de produção

## 💡 Mensagem Final

> **"Protótipos funcionam. Sistemas confiáveis duram."**

A combinação de Git, Debug/Logs e Testes é o que separa um código de estudante de um sistema profissional em produção.

## 📄 Licença

Este material é fornecido para fins educacionais.

---

**Boa aula! 🚀**
