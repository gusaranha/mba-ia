# Como Usar o Jupyter Notebook

## Opção 1: Browser (Mais Simples)

### Instalar
```bash
pip install jupyter notebook
```

### Usar
```bash
# Navegar até a pasta do projeto
cd maria_notebook

# Iniciar Jupyter
jupyter notebook

# Abre automaticamente no navegador em http://localhost:8888
# Clique em notebook_maria.ipynb para abrir
```

### Executar Células
- **Shift + Enter**: Executa célula e vai para próxima
- **Ctrl + Enter**: Executa célula e fica nela
- **Cell → Run All**: Executa todas as células

### Parar
- No terminal: **Ctrl + C** duas vezes

---

## Opção 2: VS Code

### Instalar Extensão
1. Abrir VS Code
2. Ir em Extensions (Ctrl + Shift + X)
3. Buscar "Jupyter"
4. Instalar **Jupyter** (da Microsoft)

### Instalar Jupyter
```bash
pip install jupyter ipykernel
```

### Usar
1. Abrir pasta do projeto no VS Code
2. Abrir arquivo `notebook_maria.ipynb`
3. VS Code detecta automaticamente e mostra células

### Executar Células
- Clicar no ▶️ ao lado de cada célula
- Ou **Shift + Enter**
- Ou **Run All** no topo

### Selecionar Python
- No canto superior direito, clicar em "Select Kernel"
- Escolher o Python instalado no sistema

---

## Qual Usar?

**Browser:** Funciona sempre, interface tradicional do Jupyter  
**VS Code:** Mais integrado, editor mais poderoso