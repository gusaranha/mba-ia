# Prompt para Geração de Dataset Sintético (template em brackets)

Use este prompt em qualquer ferramenta de IA (Claude, ChatGPT, Gemini etc.) para gerar
o dataset sintético do SEU projeto individual — ou para regenerar/expandir o dataset do
projeto-guia (`bos_sinteticos.csv`). Basta substituir o conteúdo entre colchetes `[ ]`.

---

## Template (com brackets, para cada aluno adaptar ao seu tema)

```
Gere um dataset sintético e 100% fictício em formato CSV para um projeto de
Machine Learning sobre [DOMÍNIO/TEMA DO PROJETO, ex.: "manutenção preditiva
de frota de viaturas"].

Contexto: [DESCREVA EM 1-2 FRASES O PROBLEMA QUE O MODELO VAI RESOLVER,
ex.: "prever se uma viatura vai precisar de manutenção corretiva nos
próximos 30 dias, a partir de dados de uso e sensores"].

Gere exatamente [NÚMERO DE REGISTROS, ex.: 40] registros, com as seguintes colunas:

1. [NOME_COLUNA_1] — tipo [TIPO_DADO, ex.: inteiro/texto/categórico/decimal/booleano/data] — [DESCRIÇÃO CURTA E, SE FOR CATEGÓRICA, LISTE OS VALORES POSSÍVEIS]
2. [NOME_COLUNA_2] — tipo [TIPO_DADO] — [DESCRIÇÃO CURTA]
3. [NOME_COLUNA_3] — tipo [TIPO_DADO] — [DESCRIÇÃO CURTA]
4. [NOME_COLUNA_4] — tipo [TIPO_DADO] — [DESCRIÇÃO CURTA]
   (adicione quantas colunas forem necessárias)

Coluna-alvo (target/rótulo que o modelo vai prever): [NOME_DA_COLUNA_ALVO],
com as categorias/valores: [LISTA DE CATEGORIAS OU FAIXA DE VALORES].

Regras importantes:
- Todos os dados devem ser fictícios — não usar nomes, locais ou casos reais.
- Distribuir os registros de forma [EQUILIBRADA ou DESBALANCEADA — escolha uma]
  entre as categorias da coluna-alvo.
- Incluir propositalmente [NÚMERO, ex.: 3 a 5] valores faltantes (vazios) em
  pelo menos uma coluna numérica, para permitir discutir tratamento de dados
  faltantes.
- Incluir propositalmente [NÚMERO, ex.: 2] outliers (valores fora do padrão)
  em pelo menos uma coluna numérica, para permitir discutir tratamento de
  outliers.
- Retornar apenas o CSV, com cabeçalho na primeira linha, separado por vírgulas,
  sem explicações adicionais.
```

---

## Versão preenchida — usada no projeto-guia `pcdf-bo-triagem`

```
Gere um dataset sintético e 100% fictício em formato CSV para um projeto de
Machine Learning sobre classificação e priorização de Boletins de Ocorrência (BO).

Contexto: a partir do relato textual de um comunicante, prever a natureza da
ocorrência (furto, roubo, estelionato etc.) para apoiar a triagem e o
roteamento mais rápido à unidade responsável.

Gere exatamente 40 registros, com as seguintes colunas:

1. id — tipo inteiro — identificador sequencial único do registro
2. texto_relato — tipo texto — relato textual fictício do comunicante, em português, descrevendo a ocorrência
3. natureza — tipo categórico — a coluna-alvo; uma das 10 categorias: Furto, Roubo, Estelionato, Ameaça, Lesão Corporal, Dano ao Patrimônio, Perturbação do Sossego, Violência Doméstica, Tráfico de Drogas, Pessoa Desaparecida
4. bairro — tipo categórico (nominal, sem ordem) — um dos 10 bairros fictícios do Distrito Federal: Asa Norte, Asa Sul, Ceilândia, Taguatinga, Samambaia, Águas Claras, Planaltina, Gama, Sobradinho, Guará
5. turno — tipo categórico (ordinal) — um de: Madrugada, Manhã, Tarde, Noite
6. dia_semana — tipo categórico — um dos 7 dias da semana
7. houve_violencia — tipo booleano — indica se houve uso de violência ou grave ameaça
8. valor_prejuizo_reais — tipo decimal — valor estimado do prejuízo financeiro em reais (0 quando não se aplica, ex.: ameaça, desaparecimento)
9. idade_vitima — tipo inteiro — idade da vítima/comunicante em anos
10. reincidencia — tipo booleano — indica se é um caso reincidente

Coluna-alvo (target/rótulo que o modelo vai prever): natureza, com as 10
categorias listadas acima.

Regras importantes:
- Todos os dados devem ser fictícios — não usar nomes, locais ou casos reais.
- Distribuir os registros de forma EQUILIBRADA entre as 10 categorias da
  coluna natureza (4 registros por categoria).
- Incluir propositalmente 4 a 5 valores faltantes (vazios) na coluna
  idade_vitima, para permitir discutir tratamento de dados faltantes.
- Incluir propositalmente 2 outliers na coluna valor_prejuizo_reais (valores
  muito acima do padrão) e 1 a 2 outliers na coluna idade_vitima (valores
  fora de uma faixa plausível), para permitir discutir tratamento de
  outliers.
- Retornar apenas o CSV, com cabeçalho na primeira linha, separado por
  vírgulas, sem explicações adicionais.
```

> Nota: o arquivo `bos_sinteticos.csv` já entregue para o projeto-guia foi gerado
> programaticamente (script `gen_dataset.py`) seguindo exatamente essa mesma
> especificação, para garantir reprodutibilidade — mas o prompt acima produz um
> resultado equivalente caso você prefira gerar via IA generativa.
