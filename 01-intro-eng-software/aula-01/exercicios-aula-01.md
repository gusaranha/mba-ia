# EXERCÍCIOS - AULA 1
## Introdução à Engenharia de Software aplicada a ML

**Data**: 04/11/2025

---

## 📝 EXERCÍCIO 1: "SOBRE MIM"

**Tempo:** 10 minutos  
**Objetivo:** Criar seu primeiro endpoint personalizado

### Tarefa

Adicione um novo endpoint à API que retorna informações sobre VOCÊ.

**Especificações:**
- **Rota:** `GET /sobre`
- **Tipo:** Endpoint GET (não recebe dados)
- **Retorno:** JSON com suas informações pessoais

### Campos obrigatórios

```json
{
  "nome": "Seu Nome Completo",
  "motivo": "Por que está fazendo o curso",
  "linguagem_principal": "Linguagem que mais usa (Python/Java/C#/PHP/etc)",
  "hobby": "Seu hobby favorito (opcional)"
}
```

### Exemplo de retorno

```json
{
  "nome": "Ana Silva",
  "motivo": "Quero colocar modelos ML em produção",
  "linguagem_principal": "Python",
  "hobby": "Fotografia"
}
```

### Onde implementar

**Arquivo:** `src/api/main.py`

### Dica inicial

```python
@app.get("/sobre")
def sobre():
    """
    Informações sobre o desenvolvedor
    """
    return {
        "nome": "SEU_NOME_AQUI",
        # ... completar
    }
```

### Como testar

1. Salvar o arquivo `main.py`
2. API deve recarregar automaticamente (se estiver com `--reload`)
3. Acessar: http://localhost:8000/sobre
4. Ou testar pelo Swagger: http://localhost:8000/docs

### Compartilhar

Após concluir, compartilhe no chat o link do seu endpoint!

---

## 📝 EXERCÍCIO 2: "CADASTRO DE PRODUTO"

**Tempo:** 15 minutos  
**Objetivo:** Criar schemas Pydantic e endpoint com validação robusta

### Tarefa

Crie um sistema de cadastro de produtos com validação automática.

### Parte 1: Criar schemas

**Arquivo:** `src/data/schemas.py`

#### Schema de entrada: `ProdutoInput`

**Campos:**
- `nome`: string, **mínimo 3 caracteres**
- `preco`: float, **maior que zero** (use `gt=0`)
- `estoque`: int, **maior ou igual a zero** (use `ge=0`)
- `descricao`: string **opcional** (use `Optional[str]`)

#### Schema de saída: `ProdutoOutput`

**Campos:**
- `id`: int (você vai gerar um ID fake)
- `nome`: str
- `preco`: float
- `status`: str (lógica: se `estoque > 0` → "disponível", senão → "esgotado")

### Parte 2: Criar endpoint

**Arquivo:** `src/api/main.py`

**Especificações:**
- **Rota:** `POST /produtos`
- **Input:** `ProdutoInput` (Pydantic valida automaticamente)
- **Output:** `ProdutoOutput`
- **Lógica:** 
  - Gerar ID fake (pode ser sempre `1` por enquanto)
  - Definir status baseado no estoque
  - Retornar `ProdutoOutput`

### Código inicial

```python
# src/data/schemas.py

from typing import Optional
from pydantic import BaseModel, Field

class ProdutoInput(BaseModel):
    """
    TODO: Adicionar validações com Field()
    """
    nome: str
    preco: float
    estoque: int
    descricao: Optional[str] = None

class ProdutoOutput(BaseModel):
    id: int
    nome: str
    preco: float
    status: str
```

```python
# src/api/main.py

@app.post("/produtos", response_model=ProdutoOutput)
def criar_produto(produto: ProdutoInput):
    """
    Cadastra novo produto com validação
    """
    # TODO: Implementar lógica
    pass
```

### Casos de teste

**✅ Caso 1: Produto válido**
```json
{
  "nome": "Mouse Gamer",
  "preco": 129.90,
  "estoque": 50,
  "descricao": "RGB 16000 DPI"
}
```
**Resultado esperado:** Status 200, produto criado com status "disponível"

**❌ Caso 2: Nome muito curto (deve falhar)**
```json
{
  "nome": "PC",
  "preco": 3000.00,
  "estoque": 5
}
```
**Resultado esperado:** Erro 422 (validação min_length)

**❌ Caso 3: Preço negativo (deve falhar)**
```json
{
  "nome": "Teclado",
  "preco": -50.00,
  "estoque": 10
}
```
**Resultado esperado:** Erro 422 (validação gt=0)

**❌ Caso 4: Estoque negativo (deve falhar)**
```json
{
  "nome": "Monitor",
  "preco": 800.00,
  "estoque": -5
}
```
**Resultado esperado:** Erro 422 (validação ge=0)

**✅ Caso 5: Estoque zero (esgotado)**
```json
{
  "nome": "Webcam",
  "preco": 250.00,
  "estoque": 0
}
```
**Resultado esperado:** Status 200, status="esgotado"

### Como testar

1. Criar os schemas em `src/data/schemas.py`
2. Importar no `main.py`: `from src.data.schemas import ProdutoInput, ProdutoOutput`
3. Implementar o endpoint
4. Testar todos os casos no Swagger UI
5. Verificar que validações funcionam automaticamente

---

## 📝 EXERCÍCIO 3: "CLASSIFICADOR DE MENSAGENS" ⭐

**Tempo:** Para fazer em casa  
**Objetivo:** Preparação para a próxima aula (integração com modelo ML real)

### Contexto

Na **Aula 2**, vamos substituir regras manuais por um **modelo ML de verdade**. Este exercício mostra a diferença entre os dois abordagens.

### Tarefa

Criar um endpoint que classifica mensagens como **SPAM** ou **NÃO SPAM** usando regras simples.

### Parte 1: Criar schemas

**Arquivo:** `src/data/schemas.py`

#### Schema de entrada: `MensagemInput`

**Campos:**
- `texto`: string (texto da mensagem)
- `tamanho`: int, maior ou igual a 0 (número de caracteres)
- `tem_link`: bool (indica se tem URL)
- `palavras_suspeitas`: lista de strings (palavras como "grátis", "ganhe", "clique")

#### Schema de saída: `ClassificacaoOutput`

**Campos:**
- `eh_spam`: bool (True se for spam)
- `confianca`: float entre 0.0 e 1.0 (confiança da classificação)
- `motivo`: string (justificativa da decisão)

### Parte 2: Implementar lógica de classificação

**Arquivo:** `src/api/main.py`

**Especificações:**
- **Rota:** `POST /classificar-mensagem`
- **Lógica:** Implementar regras simples

### Regras de classificação

A mensagem é **SPAM** se:
1. Mais de **5 palavras suspeitas**, OU
2. Tem **link** E mais de **2 palavras suspeitas**, OU
3. Mais de **1000 caracteres** E tem **link**

### Código inicial

```python
# src/data/schemas.py

from typing import List
from pydantic import BaseModel, Field

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
```

```python
# src/api/main.py

@app.post("/classificar-mensagem", response_model=ClassificacaoOutput)
def classificar_mensagem(msg: MensagemInput):
    """
    Classifica mensagem como SPAM ou não usando regras simples
    """
    logger.info(f"Classificando mensagem de {msg.tamanho} caracteres")
    
    score_spam = 0
    motivos = []
    
    # TODO: Implementar regras
    # Dica: criar score baseado nas condições
    # if len(msg.palavras_suspeitas) > 5:
    #     score_spam += ...
    #     motivos.append("...")
    
    # TODO: Decidir se é spam baseado no score
    eh_spam = score_spam >= 3  # ajustar threshold
    
    # TODO: Calcular confiança (normalizar score)
    confianca = min(score_spam / 5, 1.0)
    
    # TODO: Montar motivo final
    if eh_spam:
        motivo = "SPAM: " + ", ".join(motivos)
    else:
        motivo = "Não spam: score baixo"
    
    return ClassificacaoOutput(
        eh_spam=eh_spam,
        confianca=confianca,
        motivo=motivo
    )
```

### Casos de teste

**✅ Teste 1: Mensagem normal**
```json
{
  "texto": "Reunião amanhã às 10h",
  "tamanho": 23,
  "tem_link": false,
  "palavras_suspeitas": []
}
```
**Resultado esperado:** `eh_spam = false`

**❌ Teste 2: Spam óbvio**
```json
{
  "texto": "GANHE DINHEIRO RÁPIDO! CLIQUE AQUI PARA RECEBER PRÊMIO AGORA!",
  "tamanho": 62,
  "tem_link": true,
  "palavras_suspeitas": ["ganhe", "dinheiro", "rápido", "clique", "prêmio", "agora"]
}
```
**Resultado esperado:** `eh_spam = true`, confiança alta

**⚠️ Teste 3: Caso ambíguo**
```json
{
  "texto": "Confira as novidades no link",
  "tamanho": 29,
  "tem_link": true,
  "palavras_suspeitas": ["confira", "clique"]
}
```
**Resultado esperado:** Analisar score (pode ou não ser spam dependendo das regras)

**✅ Teste 4: Mensagem longa sem link**
```json
{
  "texto": "Lorem ipsum... (1200 caracteres)",
  "tamanho": 1200,
  "tem_link": false,
  "palavras_suspeitas": ["grátis"]
}
```
**Resultado esperado:** `eh_spam = false` (não tem link)

**❌ Teste 5: Mensagem longa COM link**
```json
{
  "texto": "Lorem ipsum... (1200 caracteres) veja mais em http://...",
  "tamanho": 1200,
  "tem_link": true,
  "palavras_suspeitas": ["clique", "veja"]
}
```
**Resultado esperado:** `eh_spam = true` (regra 3: >1000 chars + link)

### Adicionar logging

```python
logger.info(f"Classificando mensagem de {msg.tamanho} caracteres")
logger.info(f"Classificação: {'SPAM' if eh_spam else 'NÃO SPAM'} (confiança: {confianca:.2f})")
```

### Dicas de implementação

1. Use uma variável `score_spam` para acumular pontos
2. Use uma lista `motivos = []` para justificativas
3. Cada regra satisfeita adiciona pontos ao score
4. Defina um threshold (ex: `score >= 3` = spam)
5. Calcule confiança normalizando o score

### Por que este exercício é importante?

Na **Aula 2**, vamos:
1. Substituir estas regras por um **modelo ML treinado**
2. Ver como ML generaliza melhor que regras
3. Manter a mesma estrutura de API

Você verá na prática a diferença entre:
- ❌ **Regras manuais**: rígidas, não generalizam
- ✅ **Modelo ML**: aprende padrões, generaliza

### Entrega

**Não é obrigatório entregar agora!**

Este exercício é para:
- Praticar Pydantic e FastAPI
- Preparar para a Aula 2
- Entender diferença entre regras e ML

**Solução completa** será disponibilizada no repositório após a aula.

---

## 🎯 RESUMO DOS EXERCÍCIOS

| Exercício | Tipo | Tempo | Objetivo |
|-----------|------|-------|----------|
| **1 - Sobre Mim** | GET endpoint | 10 min | Criar primeiro endpoint |
| **2 - Cadastro Produto** | POST + Pydantic | 15 min | Validação robusta |
| **3 - Classificador** | POST + Lógica | Casa | Preparar para ML real |

---

## ✅ CHECKLIST DE CONCLUSÃO

### Exercício 1
- [ ] Endpoint `/sobre` criado
- [ ] Retorna JSON com informações pessoais
- [ ] Testado no navegador ou Swagger
- [ ] Compartilhado no chat

### Exercício 2
- [ ] Schemas `ProdutoInput` e `ProdutoOutput` criados
- [ ] Validações implementadas (min_length, gt, ge)
- [ ] Endpoint `/produtos` funcionando
- [ ] Todos os 5 casos de teste executados
- [ ] Validações funcionam automaticamente

### Exercício 3 (opcional)
- [ ] Schemas `MensagemInput` e `ClassificacaoOutput` criados
- [ ] Endpoint `/classificar-mensagem` implementado
- [ ] Regras de classificação funcionando
- [ ] Logging adicionado
- [ ] Pelo menos 3 casos de teste executados

---

## 📚 RECURSOS

**Documentação:**
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/


