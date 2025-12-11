# Aula 3 - Fundamentos Web, ML e API

Material de código completo da Aula 3 do curso.

## Estrutura

- **bloco2-api-rest/**: Demonstração de API com login e segurança
- **bloco2.5-fastapi/**: Exercícios e referências FastAPI/Pydantic
- **bloco3-ml-fundamentos/**: Comparação programação tradicional vs ML
- **bloco4-demo-completa/**: API completa de detecção de fraude
- **solucoes/**: Soluções comentadas dos exercícios

## Setup Rápido

```bash
# Clone ou baixe o repositório
cd aula3-codigos

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install fastapi uvicorn scikit-learn pandas numpy
```

## Como Usar

1. **Bloco 2**: Execute `api_demo.py`, abra `login.html` no navegador
2. **Bloco 2.5**: Faça os exercícios, consulte cheatsheets, compare com soluções
3. **Bloco 3**: Execute os exemplos para ver diferença tradicional vs ML
4. **Bloco 4**: Treine o modelo, execute a API, teste com exemplos

## Comandos Úteis

```bash
# Executar API
uvicorn api_demo:app --reload

# Acessar documentação
http://localhost:8000/docs
```
