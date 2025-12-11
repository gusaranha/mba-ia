# GUIA DE REFERÊNCIA - AULA 1
## Introdução à Engenharia de Software aplicada a ML

**Data**: 04/11/2025

---

## VERIFICAÇÃO INICIAL

### Verificar Python
```bash
python --version
# Deve mostrar Python 3.10+ ou 3.12
```

### Verificar pip
```bash
pip --version
```

### Verificar Git
```bash
git --version
```

---

## 1. CRIAÇÃO DA ESTRUTURA DO PROJETO

### 1.1 Criar diretório e ambiente virtual

```bash
mkdir projeto-ml-api
cd projeto-ml-api
python -m venv venv
```

### 1.2 Ativar ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 1.3 Criar estrutura de diretórios

```bash
mkdir src
mkdir src/api
mkdir src/data
mkdir src/models
mkdir tests
mkdir logs
mkdir artifacts
mkdir artifacts/models
```

### 1.4 Criar arquivos `__init__.py`

```bash
# Windows
type nul > src/__init__.py
type nul > src/api/__init__.py
type nul > src/data/__init__.py
type nul > src/models/__init__.py
type nul > tests/__init__.py

# Mac/Linux
touch src/__init__.py
touch src/api/__init__.py
touch src/data/__init__.py
touch src/models/__init__.py
touch tests/__init__.py
```

### 1.5 Criar arquivos de configuração

**Criar `.gitignore`:**
```
venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
logs/*.log
.env
*.pkl
.DS_Store
```

**Criar `requirements.txt`:**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.6.0
pytest==7.4.3
pytest-cov==4.1.0
black==24.1.1
ruff==0.1.15
mypy==1.8.0
httpx==0.26.0
scikit-learn==1.4.0
```

### 1.6 Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 2. CONFIGURAÇÃO INICIAL

### 2.1 Criar `src/config.py`

```python
import logging
from pathlib import Path

# Configurações gerais
API_VERSION = "1.0.0"
API_TITLE = "ML Model API"
API_DESCRIPTION = "API para servir modelo de Machine Learning"

# Configurações de logging
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DIR = Path("logs")

# Criar diretório de logs se não existir
LOG_DIR.mkdir(exist_ok=True)


def setup_logging():
    """
    Configura sistema de logging da aplicação
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_DIR / "app.log"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("ml_api")


# Logger global
logger = setup_logging()
logger.info("Logging configurado com sucesso")
```

---

## 3. CRIAÇÃO DA API BÁSICA COM FASTAPI

### 3.1 Criar `src/api/main.py`

```python
from fastapi import FastAPI
from src.config import API_VERSION, API_TITLE, API_DESCRIPTION, logger

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)


@app.get("/")
def root():
    """
    Endpoint raiz da API
    """
    logger.info("Endpoint raiz acessado")
    return {
        "message": "API de ML está funcionando",
        "version": API_VERSION
    }


@app.get("/health")
def health_check():
    """
    Endpoint de health check
    """
    logger.info("Health check realizado")
    return {
        "status": "healthy",
        "version": API_VERSION
    }
```

### 3.2 Executar a API

```bash
uvicorn src.api.main:app --reload
```

### 3.3 Acessar a documentação

Abrir navegador em:
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

---

## 4. SCHEMAS PYDANTIC

### 4.1 Criar `src/data/schemas.py`

```python
from pydantic import BaseModel, Field
from typing import List


class PredictionInput(BaseModel):
    """
    Schema de entrada para predição
    """
    features: List[float] = Field(
        ...,
        description="Lista de features para predição",
        min_length=4,
        max_length=4
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }


class PredictionOutput(BaseModel):
    """
    Schema de saída da predição
    """
    prediction: int = Field(..., description="Classe predita")
    probability: float = Field(..., ge=0.0, le=1.0, description="Probabilidade")
    model_version: str = Field(..., description="Versão do modelo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 0,
                "probability": 0.95,
                "model_version": "1.0.0"
            }
        }


class HealthResponse(BaseModel):
    """
    Schema de resposta do health check
    """
    status: str
    version: str
```

### 4.2 Atualizar `src/api/main.py` com Pydantic

```python
from fastapi import FastAPI, HTTPException
from src.config import API_VERSION, API_TITLE, API_DESCRIPTION, logger
from src.data.schemas import (
    PredictionInput,
    PredictionOutput,
    HealthResponse
)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)


@app.get("/")
def root():
    """
    Endpoint raiz da API
    """
    logger.info("Endpoint raiz acessado")
    return {
        "message": "API de ML está funcionando",
        "version": API_VERSION
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Endpoint de health check
    """
    logger.info("Health check realizado")
    return HealthResponse(
        status="healthy",
        version=API_VERSION
    )


@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """
    Endpoint de predição (simulado)
    """
    logger.info(f"Predição solicitada com features: {input_data.features}")
    
    # Simulação - na próxima aula será modelo real
    prediction = 0
    probability = 0.95
    
    logger.info(f"Predição: {prediction}, Probabilidade: {probability}")
    
    return PredictionOutput(
        prediction=prediction,
        probability=probability,
        model_version=API_VERSION
    )
```

---

## 5. VERSIONAMENTO COM GIT

### 5.1 Inicializar repositório

```bash
git init
```

### 5.2 Configurar Git (se ainda não configurado)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### 5.3 Adicionar e commitar arquivos

```bash
git add .
git commit -m "feat: estrutura inicial do projeto com FastAPI e Pydantic"
```

### 5.4 Verificar status

```bash
git status
git log --oneline
```

---

## 6. TESTANDO A API

### 6.1 Testar via Swagger UI

1. Acessar http://localhost:8000/docs
2. Expandir endpoint desejado
3. Clicar em "Try it out"
4. Preencher campos
5. Clicar em "Execute"
6. Verificar resposta

### 6.2 Testar via curl (opcional)

**Health check:**
```bash
curl http://localhost:8000/health
```

**Predição:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### 6.3 Verificar logs

**Terminal (console):**
- Ver logs em tempo real na janela onde uvicorn está rodando

**Arquivo:**
```bash
cat logs/app.log
# Windows: type logs\app.log
```

---

## 7. ESTRUTURA FINAL DO PROJETO

```
projeto-ml-api/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── models/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── logs/
│   └── app.log
├── artifacts/
│   └── models/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 8. COMANDOS ÚTEIS

### Ambiente Virtual

**Ativar:**
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

**Desativar:**
```bash
deactivate
```

### API

**Executar API:**
```bash
uvicorn src.api.main:app --reload
```

**Parar API:**
- `Ctrl+C` no terminal

### Git

**Status:**
```bash
git status
```

**Ver diferenças:**
```bash
git diff
```

**Adicionar arquivos:**
```bash
git add .
```

**Commit:**
```bash
git commit -m "mensagem descritiva"
```

**Ver histórico:**
```bash
git log --oneline
```

---

## 9. EXERCÍCIO 1 - "SOBRE MIM"

**Objetivo:** Criar endpoint personalizado com informações do aluno

**Adicionar em `src/api/main.py`:**

```python
@app.get("/sobre")
def sobre():
    """
    Informações sobre o desenvolvedor
    """
    return {
        "nome": "Seu Nome",
        "motivo": "Motivo para fazer o curso",
        "linguagem_principal": "Sua linguagem favorita",
        "hobby": "Seu hobby (opcional)"
    }
```

**Testar:**
1. Acessar http://localhost:8000/sobre
2. Verificar resposta no formato JSON
3. Compartilhar resultado no chat da aula

**Formato esperado:**
```json
{
  "nome": "Ana Silva",
  "motivo": "Quero colocar modelos ML em produção",
  "linguagem_principal": "Python",
  "hobby": "Fotografia"
}
```

---

## 10. EXERCÍCIO 2 - "CADASTRO DE PRODUTO"

**Objetivo:** Criar schemas e endpoint para validação de produtos

### 10.1 Criar schemas em `src/data/schemas.py`

```python
from typing import Optional

class ProdutoInput(BaseModel):
    """
    Schema de entrada para cadastro de produto
    """
    nome: str = Field(..., min_length=3, description="Nome do produto")
    preco: float = Field(..., gt=0, description="Preço maior que zero")
    estoque: int = Field(..., ge=0, description="Estoque não-negativo")
    descricao: Optional[str] = Field(None, description="Descrição opcional")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Mouse Gamer",
                "preco": 129.90,
                "estoque": 50,
                "descricao": "RGB 16000 DPI"
            }
        }


class ProdutoOutput(BaseModel):
    """
    Schema de saída do cadastro
    """
    id: int
    nome: str
    preco: float
    status: str
```

### 10.2 Criar endpoint em `src/api/main.py`

```python
@app.post("/produtos", response_model=ProdutoOutput)
def criar_produto(produto: ProdutoInput):
    """
    Cadastra novo produto com validação
    """
    # Gera ID fake (em produção viria do banco)
    produto_id = 1
    
    # Define status baseado no estoque
    status = "disponível" if produto.estoque > 0 else "esgotado"
    
    return ProdutoOutput(
        id=produto_id,
        nome=produto.nome,
        preco=produto.preco,
        status=status
    )
```

### 10.3 Testar casos

**Caso 1: Produto válido**
```json
{
  "nome": "Mouse Gamer",
  "preco": 129.90,
  "estoque": 50,
  "descricao": "RGB 16000 DPI"
}
```
Resultado esperado: Status 200, produto criado

**Caso 2: Nome muito curto**
```json
{
  "nome": "PC",
  "preco": 3000.00,
  "estoque": 5
}
```
Resultado esperado: Erro 422 (min_length=3)

**Caso 3: Preço negativo**
```json
{
  "nome": "Teclado",
  "preco": -50.00,
  "estoque": 10
}
```
Resultado esperado: Erro 422 (gt=0)

**Caso 4: Estoque negativo**
```json
{
  "nome": "Monitor",
  "preco": 800.00,
  "estoque": -5
}
```
Resultado esperado: Erro 422 (ge=0)

**Caso 5: Estoque zero (esgotado)**
```json
{
  "nome": "Webcam",
  "preco": 250.00,
  "estoque": 0
}
```
Resultado esperado: Status 200, status="esgotado"

---

## 11. EXERCÍCIO 3 (PARA CASA) - CLASSIFICADOR DE MENSAGENS

### 11.1 Criar schemas em `src/data/schemas.py`

```python
class MensagemInput(BaseModel):
    """
    Schema para classificação de mensagens
    """
    texto: str = Field(..., description="Texto da mensagem")
    tamanho: int = Field(..., ge=0, description="Número de caracteres")
    tem_link: bool = Field(..., description="Indica se mensagem tem link")
    palavras_suspeitas: List[str] = Field(
        default_factory=list,
        description="Lista de palavras suspeitas detectadas"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "texto": "Ganhe dinheiro rápido! Clique aqui",
                "tamanho": 37,
                "tem_link": True,
                "palavras_suspeitas": ["ganhe", "dinheiro", "rápido", "clique"]
            }
        }


class ClassificacaoOutput(BaseModel):
    """
    Schema de saída da classificação
    """
    eh_spam: bool = Field(..., description="Se mensagem é spam")
    confianca: float = Field(..., ge=0.0, le=1.0, description="Confiança da classificação")
    motivo: str = Field(..., description="Justificativa da classificação")
    
    class Config:
        json_schema_extra = {
            "example": {
                "eh_spam": True,
                "confianca": 0.85,
                "motivo": "4 palavras suspeitas detectadas e presença de link"
            }
        }
```

### 11.2 Criar endpoint em `src/api/main.py`

```python
@app.post("/classificar-mensagem", response_model=ClassificacaoOutput)
def classificar_mensagem(msg: MensagemInput):
    """
    Classifica mensagem como SPAM ou não usando regras simples
    
    Regras:
    - SPAM se > 5 palavras suspeitas
    - SPAM se (tem link E > 2 palavras suspeitas)
    - SPAM se (> 1000 caracteres E tem link)
    """
    logger.info(f"Classificando mensagem de {msg.tamanho} caracteres")
    
    score_spam = 0
    motivos = []
    
    # Regra 1: Muitas palavras suspeitas
    if len(msg.palavras_suspeitas) > 5:
        score_spam += 3
        motivos.append(f"{len(msg.palavras_suspeitas)} palavras suspeitas (>5)")
    elif len(msg.palavras_suspeitas) > 2:
        score_spam += 2
        motivos.append(f"{len(msg.palavras_suspeitas)} palavras suspeitas")
    
    # Regra 2: Link com palavras suspeitas
    if msg.tem_link and len(msg.palavras_suspeitas) > 2:
        score_spam += 2
        motivos.append("Link presente com palavras suspeitas")
    
    # Regra 3: Mensagem muito longa com link
    if msg.tamanho > 1000 and msg.tem_link:
        score_spam += 1
        motivos.append("Mensagem longa (>1000 chars) com link")
    
    # Decisão
    eh_spam = score_spam >= 3
    confianca = min(score_spam / 5, 1.0)  # Normalizar para 0-1
    
    if eh_spam:
        motivo = "SPAM: " + ", ".join(motivos)
    else:
        motivo = "Não spam: score baixo"
    
    logger.info(f"Classificação: {'SPAM' if eh_spam else 'NÃO SPAM'} (confiança: {confianca:.2f})")
    
    return ClassificacaoOutput(
        eh_spam=eh_spam,
        confianca=confianca,
        motivo=motivo
    )
```

### 11.3 Casos de teste

**Teste 1: Mensagem normal**
```json
{
  "texto": "Reunião amanhã às 10h",
  "tamanho": 23,
  "tem_link": false,
  "palavras_suspeitas": []
}
```
Resultado esperado: `eh_spam = false`

**Teste 2: Spam óbvio**
```json
{
  "texto": "GANHE DINHEIRO RÁPIDO! CLIQUE AQUI PARA RECEBER PRÊMIO AGORA!",
  "tamanho": 62,
  "tem_link": true,
  "palavras_suspeitas": ["ganhe", "dinheiro", "rápido", "clique", "prêmio", "agora"]
}
```
Resultado esperado: `eh_spam = true`

**Teste 3: Caso ambíguo**
```json
{
  "texto": "Confira as novidades no link",
  "tamanho": 29,
  "tem_link": true,
  "palavras_suspeitas": ["confira", "clique"]
}
```
Resultado esperado: Deve analisar score

---

## 12. PRÓXIMA AULA

**Data:** 06/11/2025 (quinta-feira)

**Tópicos:**
- Receber modelo ML pré-treinado (.pkl)
- Carregar modelo eficientemente (Singleton pattern)
- Integrar modelo com API
- Boas práticas: black, ruff, mypy
- Refatoração em módulos

**Preparação recomendada:**
- Revisar código da Aula 1
- Fazer Exercício 3 (classificador)
- Testar todos endpoints criados
- Commit do código no Git

---

## 13. TROUBLESHOOTING

### API não inicia
- Verificar se porta 8000 está livre
- Verificar se ambiente virtual está ativado
- Verificar erros de sintaxe no código

### Erro de import
- Verificar estrutura de diretórios
- Verificar presença de `__init__.py`
- Executar comando do diretório raiz do projeto

### Validação não funciona
- Verificar se model importado corretamente
- Verificar tipos dos campos no schema
- Ver mensagem de erro no Swagger

### Logs não aparecem
- Verificar se `setup_logging()` foi chamado
- Verificar se diretório `logs/` existe
- Verificar permissões de escrita

### Git não funciona
- Verificar se Git está instalado
- Configurar user.name e user.email
- Verificar se está no diretório correto

---

## 14. COMANDOS DE VERIFICAÇÃO FINAL

```bash
# Verificar estrutura
ls -la  # Mac/Linux
dir     # Windows

# Verificar ambiente virtual ativo
which python    # Mac/Linux
where python    # Windows
# Deve mostrar caminho com 'venv'

# Verificar pacotes instalados
pip list

# Verificar API funcionando
curl http://localhost:8000/health

# Verificar logs
tail -f logs/app.log  # Mac/Linux
type logs\app.log     # Windows

# Verificar commits Git
git log --oneline
```

---

**FIM DO GUIA DE REFERÊNCIA - AULA 1**
