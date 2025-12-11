# GUIA DE SETUP PRÉVIO
## Introdução à Engenharia de Software aplicada a ML

---

Este guia vai preparar seu ambiente de desenvolvimento antes do início das aulas. Dedique 2-3 horas para completar todas as etapas.

---

# PARTE 1: SETUP DO AMBIENTE

## 1.1 Instalação do Python 3.12

### Windows

1. Acesse: https://www.python.org/downloads/
2. Baixe **Python 3.12**
3. **IMPORTANTE**: Marque "Add Python to PATH" durante instalação
4. Verifique a instalação:
```bash
python --version
# Deve mostrar: Python 3.12.x
```

**Troubleshooting Windows**:
- Se `python` não for encontrado, tente `py --version`
- Problema de PATH: Adicione manualmente `C:\Python312` ao PATH do sistema
- Reinicie o terminal após instalação

### macOS

**Opção 1: Homebrew (recomendado)**
```bash
# Instalar Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3.12
brew install python@3.12
```

**Opção 2: Site oficial**
- Baixe de https://www.python.org/downloads/mac-osx/
- Instale o pacote .pkg

**Verificação**:
```bash
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
python3 --version
```

## 1.2 Ambiente Virtual (venv)

Ambientes virtuais isolam dependências do projeto.

**Criar ambiente virtual**:
```bash
# Navegar para pasta do projeto
mkdir projeto-ml-api
cd projeto-ml-api

# Criar venv
python -m venv venv
```

**Ativar ambiente virtual**:

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

**Quando ativado**, você verá `(venv)` no início da linha do terminal.

**Desativar** (quando terminar):
```bash
deactivate
```

## 1.3 Gerenciador de Pacotes - pip

O pip já vem com Python. Atualize-o:

```bash
python -m pip install --upgrade pip
```

**Instalar pacote exemplo**:
```bash
pip install requests
```

**Listar pacotes instalados**:
```bash
pip list
```

**Verificação**:
```bash
pip --version
# Deve mostrar versão 23.x ou superior
```

## 1.4 Git - Versionamento de Código

### Windows
- Baixe de: https://git-scm.com/download/win
- Instale com opções padrão
- Reinicie terminal

### macOS
```bash
brew install git
```

### Linux
```bash
sudo apt install git
```

**Configuração inicial**:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

**Verificação**:
```bash
git --version
```

**Comandos essenciais que usaremos**:
```bash
git clone <url>          # Copiar repositório
git add .                # Adicionar mudanças
git commit -m "mensagem" # Salvar versão
git push                 # Enviar para servidor
git status               # Ver estado atual
```

## 1.5 VS Code - Editor de Código

**Download**: https://code.visualstudio.com/

### Extensões Essenciais

Após instalar VS Code, adicione estas extensões:

1. **Python** (Microsoft)
   - Busque "Python" no marketplace de extensões
   - Clique Install

2. **Pylance** (Microsoft)
   - Análise de código e autocompletar
   - Geralmente instalada com extensão Python

**Opcional mas recomendado**:
- **Black Formatter** - formatação automática
- **GitLens** - melhor visualização Git

### Configurar VS Code para Python

1. Abra VS Code
2. Abra pasta do projeto: `File > Open Folder`
3. Selecione interpretador Python:
   - `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)
   - Digite "Python: Select Interpreter"
   - Escolha o Python do venv (mostrará caminho com `venv`)

## 1.6 Instalação de Pacotes Principais

Com venv ativado, instale pacotes que usaremos no curso:

```bash
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install pydantic==2.6.0
pip install pytest==7.4.3
pip install pytest-cov==4.1.0
pip install black==24.1.1
pip install ruff==0.1.15
pip install mypy==1.8.0
pip install httpx==0.26.0
pip install scikit-learn==1.4.0
```

**Ou crie arquivo `requirements.txt`**:
```txt
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

E instale tudo de uma vez:
```bash
pip install -r requirements.txt
```

## 1.7 Verificação Final do Ambiente

Execute estes comandos para confirmar que tudo está funcionando:

```bash
# Python
python --version

# pip
pip --version

# Git
git --version

# Verificar pacotes instalados
pip show fastapi
pip show pytest
```

**Teste rápido FastAPI**:

Crie arquivo `test_api.py`:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Setup funcionando!"}
```

Execute:
```bash
uvicorn test_api:app --reload
```

Abra navegador em: http://localhost:8000

Se ver `{"message": "Setup funcionando!"}`, está tudo OK! ✅

---

# PARTE 2: PYTHON PARA DESENVOLVEDORES DE OUTRAS LINGUAGENS

Se você vem de C#, Java, PHP ou outras linguagens, esta seção vai acelerar seu aprendizado de Python mostrando equivalências diretas.

## 2.1 Diferenças Fundamentais

### Indentação é Sintaxe

**C#/Java/PHP** usam chaves `{}`:
```csharp
if (x > 0) {
    Console.WriteLine("Positivo");
}
```

**Python** usa indentação (4 espaços):
```python
if x > 0:
    print("Positivo")
```

⚠️ **IMPORTANTE**: Misturar tabs e espaços causa erro. Use sempre 4 espaços.

### Tipagem Dinâmica

**C#** (tipagem estática):
```csharp
int idade = 25;
string nome = "Ana";
```

**Python** (tipagem dinâmica):
```python
idade = 25        # Python infere que é int
nome = "Ana"      # Python infere que é str
```

Python descobre o tipo automaticamente, mas você pode adicionar type hints (veremos adiante).

### None vs null/nil

**C#/Java**: `null`
**PHP**: `null`
**Python**: `None`

```python
resultado = None  # equivalente a null

if resultado is None:
    print("Sem resultado")
```

Use `is None` e `is not None`, não `== None`.

### Tudo é Objeto

Em Python, até funções e números são objetos:

```python
x = 5
print(type(x))  # <class 'int'>

def funcao():
    pass

print(type(funcao))  # <class 'function'>
```

## 2.2 Sintaxe Lado-a-Lado

### Tabela de Equivalências

| Conceito | C# / Java | Python |
|----------|-----------|--------|
| Declaração de variável | `int x = 10;` | `x = 10` |
| String | `string s = "oi";` | `s = "oi"` |
| Array/Lista | `int[] arr = {1,2,3};` | `arr = [1, 2, 3]` |
| Dicionário | `Dictionary<K,V>` | `dict[K, V]` ou `{"key": 1}` |
| Boolean | `bool flag = true;` | `flag = True` |
| Null | `null` | `None` |
| Concatenar strings | `"Hi " + name` | `"Hi " + name` ou `f"Hi {name}"` |
| Condição | `if (x > 0) { }` | `if x > 0:` |
| Loop for | `for (int i=0; i<10; i++)` | `for i in range(10):` |
| Loop foreach | `foreach (var x in arr)` | `for x in arr:` |
| Função | `int Calc(int a) { return a*2; }` | `def calc(a): return a*2` |
| Classe | `public class Foo { }` | `class Foo:` |
| Herança | `: BaseClass` | `(BaseClass)` |
| Try/catch | `try { } catch (Ex e) { }` | `try: ... except Ex as e:` |

### Exemplos Práticos

**Variáveis e Tipos Básicos**:

C#:
```csharp
int quantidade = 100;
double preco = 29.99;
string produto = "Mouse";
bool disponivel = true;
```

Python:
```python
quantidade = 100
preco = 29.99
produto = "Mouse"
disponivel = True  # T maiúsculo!
```

**Funções**:

Java:
```java
public int calcularTotal(int quantidade, double preco) {
    return quantidade * preco;
}
```

Python:
```python
def calcular_total(quantidade, preco):
    return quantidade * preco
```

**Condicionais**:

PHP:
```php
if ($idade >= 18) {
    echo "Maior de idade";
} else {
    echo "Menor de idade";
}
```

Python:
```python
if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")
```

**Loops**:

C#:
```csharp
// For tradicional
for (int i = 0; i < 10; i++) {
    Console.WriteLine(i);
}

// Foreach
foreach (var item in lista) {
    Console.WriteLine(item);
}
```

Python:
```python
# Equivalente ao for tradicional
for i in range(10):
    print(i)

# Equivalente ao foreach
for item in lista:
    print(item)
```

## 2.3 Type Hints (Familiar para C#/Java)

Python permite adicionar anotações de tipo (opcional, mas recomendado):

**Sem type hints**:
```python
def calcular_preco(quantidade, preco_unitario):
    return quantidade * preco_unitario
```

**Com type hints** (parece C#/Java):
```python
def calcular_preco(quantidade: int, preco_unitario: float) -> float:
    return quantidade * preco_unitario
```

**Tipos comuns**:
```python
from typing import List, Dict, Optional, Tuple

nome: str = "Ana"
idade: int = 25
altura: float = 1.75
ativo: bool = True

# Listas tipadas
numeros: List[int] = [1, 2, 3, 4]
nomes: List[str] = ["Ana", "João"]

# Dicionários tipados
precos: Dict[str, float] = {"maçã": 2.50, "banana": 1.80}

# Opcional (pode ser None)
resultado: Optional[int] = None

# Tupla
coordenadas: Tuple[float, float] = (10.5, 20.3)
```

## 2.4 Imports e Módulos

**C#**:
```csharp
using System;
using System.Collections.Generic;
```

**Java**:
```java
import java.util.ArrayList;
import java.util.HashMap;
```

**Python**:
```python
import datetime
import json

# Import específico
from datetime import datetime
from typing import List, Dict

# Import com alias
import numpy as np
import pandas as pd
```

## 2.5 Idiomatismos Python

### List Comprehension

Ao invés de loops tradicionais, Python tem sintaxe compacta:

**C#** (LINQ):
```csharp
var squares = numbers.Select(x => x * x).ToList();
```

**Python** (list comprehension):
```python
squares = [x**2 for x in numbers]
```

**Mais exemplos**:
```python
# Filtrar e transformar
pares = [x for x in range(10) if x % 2 == 0]
# Resultado: [0, 2, 4, 6, 8]

# Strings maiúsculas
nomes_upper = [nome.upper() for nome in nomes]
```

### Context Managers (with)

Equivalente a `using` em C# - gerenciamento automático de recursos:

**C#**:
```csharp
using (var file = File.OpenRead("data.txt")) {
    // Usa arquivo
}  // Fecha automaticamente
```

**Python**:
```python
with open('data.txt') as f:
    data = f.read()
# Fecha automaticamente
```

### Multiple Assignment

```python
# Trocar valores sem variável temporária
a, b = 1, 2
a, b = b, a  # Agora a=2, b=1

# Unpacking
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5
```

### Dictionary Methods

```python
# Get com valor default (evita KeyError)
preco = precos.get('produto', 0.0)

# Verificar se chave existe
if 'produto' in precos:
    print(precos['produto'])

# Iterar dicionário
for chave, valor in precos.items():
    print(f"{chave}: {valor}")
```

## 2.6 Gotchas Comuns por Linguagem

### Para Desenvolvedores C#

**Propriedades** - use decorator `@property`:

C#:
```csharp
public class Pessoa {
    private string _nome;
    public string Nome {
        get { return _nome; }
        set { _nome = value; }
    }
}
```

Python:
```python
class Pessoa:
    def __init__(self):
        self._nome = ""
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, value):
        self._nome = value

# Uso
p = Pessoa()
p.nome = "Ana"  # Usa setter
print(p.nome)   # Usa getter
```

**Async/await** - Python tem sintaxe similar:
```python
async def buscar_dados():
    resultado = await chamada_api()
    return resultado
```

### Para Desenvolvedores Java

**Sem sobrecarga de métodos** - use argumentos default ou `*args`:

Java:
```java
public void processar(int x) { }
public void processar(int x, int y) { }
```

Python:
```python
def processar(x, y=None):
    if y is None:
        # Versão com 1 argumento
    else:
        # Versão com 2 argumentos
```

**Interfaces** - use classes abstratas ou Protocols:
```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def save(self, data):
        pass

# Ou Protocol (Python 3.8+)
from typing import Protocol

class Repository(Protocol):
    def save(self, data) -> None:
        ...
```

### Para Desenvolvedores PHP

**Sem `$` em variáveis**:

PHP:
```php
$nome = "Ana";
$idade = 25;
echo "$nome tem $idade anos";
```

Python:
```python
nome = "Ana"
idade = 25
print(f"{nome} tem {idade} anos")
```

**Operador de objeto**:

PHP: `$objeto->metodo()`
Python: `objeto.metodo()`

**Arrays associativos = dicionários**:

PHP:
```php
$pessoa = array(
    "nome" => "Ana",
    "idade" => 25
);
echo $pessoa["nome"];
```

Python:
```python
pessoa = {
    "nome": "Ana",
    "idade": 25
}
print(pessoa["nome"])
```

## 2.7 Convenções Python (PEP 8)

### Nomenclatura

**Importante**: Python usa `snake_case`, não `camelCase`!

| Tipo | C#/Java | Python (PEP 8) |
|------|---------|----------------|
| Função/Método | `calcularTotal()` | `calcular_total()` |
| Variável | `nomeCompleto` | `nome_completo` |
| Classe | `PessoaFisica` | `PessoaFisica` (igual!) |
| Constante | `MAX_VALUE` | `MAX_VALUE` (igual!) |
| Privado | `private _value` | `_value` (convenção) |

**Exemplos**:
```python
# ✅ Correto (PEP 8)
def calcular_preco_total(quantidade, preco_unitario):
    return quantidade * preco_unitario

nome_usuario = "ana.silva"
MAX_TENTATIVAS = 3

class GerenciadorProdutos:
    def __init__(self):
        self._estoque_privado = {}

# ❌ Evitar (estilo não-Python)
def CalcularPrecoTotal(quantidade, precoUnitario):  # Não use PascalCase/camelCase
    return quantidade * precoUnitario
```

### Outras Convenções

**Indentação**: 4 espaços (nunca tabs)
**Linhas**: máximo 79-100 caracteres
**Espaços em branco**:
```python
# ✅ Correto
x = 1
lista = [1, 2, 3]
resultado = funcao(a, b)

# ❌ Evitar
x=1
lista=[1,2,3]
resultado=funcao( a,b )
```

## 2.8 Teste Seu Conhecimento

Execute estes snippets no terminal Python interativo (`python`):

```python
# 1. Variáveis e tipos
nome = "Python"
versao = 3.12
print(f"{nome} versão {versao}")

# 2. List comprehension
numeros = [1, 2, 3, 4, 5]
quadrados = [n**2 for n in numeros]
print(quadrados)

# 3. Dicionário
pessoa = {"nome": "Ana", "idade": 30}
print(pessoa.get("nome"))

# 4. Função com type hints
def somar(a: int, b: int) -> int:
    return a + b

print(somar(5, 3))

# 5. Context manager
with open("teste.txt", "w") as f:
    f.write("Hello Python!")

# 6. Condicionais Python
idade = 20
status = "adulto" if idade >= 18 else "menor"
print(status)
```

---

## CHECKLIST FINAL

Antes da Aula 1, certifique-se que:

- [ ] Python 3.12 instalado e verificado (`python --version`)
- [ ] Ambiente virtual criado e testado
- [ ] pip funcionando (`pip --version`)
- [ ] Git instalado e configurado
- [ ] VS Code instalado com extensão Python
- [ ] Pacotes principais instalados (FastAPI, pytest, etc)
- [ ] Teste rápido de FastAPI funcionou
- [ ] Entendeu diferenças básicas de sintaxe Python
- [ ] Revisou convenções PEP 8 (snake_case)
- [ ] Executou snippets de código Python

---

## PROBLEMAS COMUNS E SOLUÇÕES

### "python não é reconhecido como comando"
**Windows**: Use `py` ao invés de `python`, ou adicione Python ao PATH
**Mac/Linux**: Use `python3` ao invés de `python`

### "pip não encontrado"
```bash
python -m pip --version
# Use sempre: python -m pip install <pacote>
```

### "Permission denied" no Linux/Mac
```bash
# Não use sudo! Use venv:
python3 -m venv venv
source venv/bin/activate
pip install <pacote>
```

### VS Code não encontra interpretador Python
1. `Ctrl+Shift+P` > "Python: Select Interpreter"
2. Escolha o Python que está dentro da pasta `venv`
3. Reinicie VS Code se necessário

### Erros de indentação
- Configure VS Code para usar 4 espaços
- Não misture tabs e espaços
- Ative "View > Render Whitespace" para visualizar

---

## RECURSOS ADICIONAIS

**Documentação Oficial**:
- Python: https://docs.python.org/3/
- FastAPI: https://fastapi.tiangolo.com/
- Pytest: https://docs.pytest.org/

**Tutoriais Interativos**:
- Real Python: https://realpython.com/
- Python Tutor (visualizador): https://pythontutor.com/

**Para Desenvolvedores**:
- Python para programadores Java: https://realpython.com/oop-in-python-vs-java/
- Python para programadores C#: https://python.readthedocs.io/

