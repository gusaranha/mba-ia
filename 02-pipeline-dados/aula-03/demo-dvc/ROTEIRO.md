# Roteiro de Demonstração: DVC na Prática

## Preparação (antes da aula)

```bash
# 1. Instalar dependências
pip install dvc pandas numpy scikit-learn

# 2. Ir para a pasta do projeto
cd demo-dvc

# 3. Gerar dados
python gerar_dados.py
```

---

## PARTE 1: Setup (5 min)

### Passo 1.1: Inicializar Git

**Fale:** "Primeiro, precisamos de um repositório Git. DVC trabalha junto com Git."

```bash
git init
```

**Mostre:** Pasta `.git` criada.

---

### Passo 1.2: Inicializar DVC

**Fale:** "Agora inicializamos o DVC. Ele vai criar sua própria estrutura."

```bash
dvc init
```

**Mostre:** Pasta `.dvc` criada.

**Fale:** "O DVC criou arquivos de configuração. Vamos commitar isso."

```bash
git add .dvc .dvcignore
git commit -m "Inicializa DVC"
```

---

### Passo 1.3: Configurar Storage

**Fale:** "DVC precisa saber ONDE guardar os arquivos grandes. Em produção seria S3, Google Cloud. Para demo, vamos usar uma pasta local."

```bash
mkdir -p /tmp/dvc-storage
dvc remote add -d storage /tmp/dvc-storage
```

**Fale:** "O `-d` significa 'default'. É o storage padrão."

```bash
git add .dvc/config
git commit -m "Configura storage remoto"
```

---

## PARTE 2: Versionar Dados v1 (10 min)

### Passo 2.1: Ver tamanho do arquivo

**Fale:** "Vamos ver quantos dados temos."

```bash
wc -l data/transacoes.csv
```

**Esperado:** 150.001 linhas (150k + cabeçalho)

**Fale:** "150 mil transações. Se colocarmos direto no Git, cada versão ocupa esse espaço todo."

---

### Passo 2.2: Adicionar ao DVC

**Fale:** "Em vez de `git add`, usamos `dvc add`."

```bash
dvc add data/transacoes.csv
```

**Mostre o output:** DVC criou arquivo `.dvc`

**Fale:** "O que aconteceu? Vamos ver."

```bash
ls data/
```

**Mostre:** `transacoes.csv`, `transacoes.csv.dvc`, `.gitignore`

---

### Passo 2.3: Ver o ponteiro

**Fale:** "Este arquivo `.dvc` é o PONTEIRO. É isso que vai pro Git."

```bash
cat data/transacoes.csv.dvc
```

**Mostre e explique:**
```yaml
outs:
- md5: a1b2c3d4...    # ← Hash único (impressão digital)
  size: 12345678      # ← Tamanho em bytes
  path: transacoes.csv
```

**Fale:** "O hash MD5 é como CPF do arquivo. Dois iguais = mesmo hash. Qualquer mudança = hash diferente."

---

### Passo 2.4: Ver o .gitignore

**Fale:** "O DVC também criou um .gitignore."

```bash
cat data/.gitignore
```

**Mostre:** `/transacoes.csv`

**Fale:** "O arquivo grande está IGNORADO pelo Git. Só o ponteiro vai pro repositório."

---

### Passo 2.5: Commitar ponteiro

**Fale:** "Agora commitamos o ponteiro no Git."

```bash
git add data/transacoes.csv.dvc data/.gitignore
git commit -m "Dados v1 - 150k transacoes"
```

---

### Passo 2.6: Enviar dados para storage

**Fale:** "O commit foi só do ponteiro. Os dados reais precisam ir pro storage."

```bash
dvc push
```

**Fale:** "Agora os dados estão no storage. Qualquer pessoa que clonar pode baixar."

---

## PARTE 3: Treinar e Versionar Modelo v1 (5 min)

### Passo 3.1: Executar treino

**Fale:** "Vamos treinar o modelo com esses dados."

```bash
python treinar_modelo.py
```

**Mostre:** Logs do treinamento, F1 obtido (~0.50)

---

### Passo 3.2: Versionar modelo

**Fale:** "Mesmo processo para o modelo."

```bash
dvc add models/modelo_em_producao.pkl
git add models/modelo_em_producao.pkl.dvc models/.gitignore
git commit -m "Modelo v1 - F1=0.50"
dvc push
```

---

### Passo 3.3: Ver histórico

**Fale:** "Vamos ver nosso histórico."

```bash
git log --oneline
```

**Mostre:**
```
abc1234 Modelo v1 - F1=0.50
def5678 Dados v1 - 150k transacoes
ghi9012 Configura storage remoto
jkl3456 Inicializa DVC
```

**Fale:** "Cada commit tem código E ponteiros. Tudo vinculado."

---

## PARTE 4: Simular Nova Semana (10 min)

### Passo 4.1: Adicionar dados novos

**Fale:** "Passou uma semana. Chegaram dados de novembro."

```bash
cat data/novembro.csv >> data/transacoes.csv
wc -l data/transacoes.csv
```

**Esperado:** ~200.000 linhas

**Fale:** "Agora temos 200 mil transações."

---

### Passo 4.2: Versionar dados atualizados

```bash
dvc add data/transacoes.csv
```

**Fale:** "O hash mudou porque o arquivo mudou."

```bash
cat data/transacoes.csv.dvc
```

**Mostre:** Hash diferente do anterior.

```bash
git add data/transacoes.csv.dvc
git commit -m "Dados v2 - 200k transacoes"
dvc push
```

---

### Passo 4.3: Re-treinar modelo

```bash
python treinar_modelo.py
```

**Mostre:** Comparação de F1

```bash
dvc add models/modelo_em_producao.pkl
git add models/modelo_em_producao.pkl.dvc
git commit -m "Modelo v2"
dvc push
```

---

### Passo 4.4: Ver histórico completo

```bash
git log --oneline
```

**Mostre:**
```
mno7890 Modelo v2
pqr1234 Dados v2 - 200k transacoes
abc1234 Modelo v1 - F1=0.50
def5678 Dados v1 - 150k transacoes
...
```

**Fale:** "Cada modelo sabe com quais dados foi treinado. Rastreabilidade!"

---

## PARTE 5: Navegar no Tempo (10 min)

### Passo 5.1: Estado atual

**Fale:** "Quantas linhas temos agora?"

```bash
wc -l data/transacoes.csv
```

**Esperado:** ~200.000

---

### Passo 5.2: Voltar para v1

**Fale:** "Quero voltar para 150 mil. Primeiro, acho o commit."

```bash
git log --oneline
```

**Pegue o hash do "Dados v1"** (ex: def5678)

```bash
git checkout def5678 -- data/transacoes.csv.dvc
```

**Fale:** "Voltei o PONTEIRO. Mas o arquivo ainda não mudou."

```bash
wc -l data/transacoes.csv
```

**Ainda mostra:** ~200.000

---

### Passo 5.3: Sincronizar arquivo

**Fale:** "Preciso sincronizar o arquivo com o ponteiro."

```bash
dvc checkout
```

```bash
wc -l data/transacoes.csv
```

**Agora mostra:** ~150.000

**Fale:** "Voltou! O DVC buscou a versão antiga do storage."

---

### Passo 5.4: Restaurar versão atual

**Fale:** "Vamos voltar para o presente."

```bash
git checkout HEAD -- data/transacoes.csv.dvc
dvc checkout
wc -l data/transacoes.csv
```

**Mostra:** ~200.000

**Fale:** "De volta ao estado atual."

---

## PARTE 6: Resumo (2 min)

### Mostrar comparação

```bash
du -sh .git
du -sh /tmp/dvc-storage
```

**Fale:** "Repositório Git pequeno. Dados grandes no storage separado."

### Pontos-chave

1. **Git guarda ponteiros** (~1KB cada)
2. **DVC guarda dados** (no storage)
3. **Cada commit sabe** qual versão dos dados
4. **Navegação:** `git checkout` + `dvc checkout`
5. **Reprodutibilidade** pelo hash

---

## Comandos Resumo

```bash
# Setup (uma vez)
dvc init
dvc remote add -d storage <caminho>

# Versionar
dvc add <arquivo>
git add <arquivo>.dvc
git commit -m "mensagem"
dvc push

# Colaborar
git clone <repo>
dvc pull

# Navegar
git checkout <hash> -- <arquivo>.dvc
dvc checkout
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| DVC não encontrado | `pip install dvc` |
| Remote not configured | `dvc remote add -d storage /tmp/dvc-storage` |
| Arquivo não voltou | Fazer os 2 passos: `git checkout` + `dvc checkout` |
