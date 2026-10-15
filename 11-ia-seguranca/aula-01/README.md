# Circuito: loja fictícia para a aula 00 de LLM e MCP

Aplicação **Flask + SQLite** pronta para distribuição aos alunos. Inclui catálogo de nove eletrônicos, busca, filtro por categoria, carrinho, registro de pedidos fictícios e painel de vendas. Não há pagamento, cobrança, entrega real, cadastro de clientes ou coleta de dados pessoais.

A aula apresenta IA clássica e generativa, LLMs e seus limites e a utilidade do MCP ao permitir que o modelo use ferramentas para agir. Na prática, os alunos implementam um MCP sobre a loja virtual de exemplo. Os alunos recebem o site e o banco prontos, e seu desenvolvimento fica fora da aula.

## Implementação do MCP durante a aula

O `servidor_mcp.py` fornecido é uma referência completa para o professor e para consulta dos alunos. Para praticar a implementação, renomeie-o para `servidor_mcp_referencia.py` e crie seu próprio `servidor_mcp.py` com o exemplo dos slides. Exponha as funções já prontas de `consultas.py` como tools: `listar_produtos`, `produtos_mais_vendidos`, `valor_medio` e `vendas_ultimas_24h`.

Mantenha os nomes e argumentos apresentados no material e coloque `mcp.run(transport="stdio")` depois das definições das ferramentas. O cliente Python e a configuração do OpenCode usarão o arquivo `servidor_mcp.py` implementado pelo aluno. As consultas e o site já estão prontos, para concentrar a programação no MCP.

## Preparação antes da aula

Requisito: Python 3.12 instalado. Extraia o pacote em uma pasta local. No Windows, abra um terminal nessa pasta e execute:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -c constraints_testadas.txt
.\.venv\Scripts\python.exe banco.py --atualizar-datas
.\.venv\Scripts\python.exe configurar_opencode.py
```

Se o comando `py` não existir, use o caminho do Python instalado, por exemplo `python -m venv .venv`. Não é necessário ativar o ambiente virtual. Em Linux/macOS, crie o ambiente com `python3 -m venv .venv` e substitua `.venv\Scripts\python.exe` por `.venv/bin/python`.

O banco `dados/loja.sqlite3` já acompanha o pacote com dados sintéticos. Se esse arquivo estiver ausente, `banco.py`, o Flask e o servidor MCP o criam automaticamente com nove produtos e 60 pedidos fictícios. O histórico inicial inclui pedidos nas últimas 24 horas e nos últimos sete dias.

`--atualizar-datas` aproxima o histórico do momento da aula, preservando o intervalo entre os pedidos. Execute uma vez antes da prática. Ele desloca **todas** as datas, inclusive vendas simuladas anteriormente. Não execute durante comparações antes/depois. Para começar novamente com a base de referência, extraia outra cópia do pacote.

O professor deve preparar também o OpenCode e seu provedor/modelo antes do encontro. A loja e o cliente Python funcionam sem chave de API. O uso de um modelo no OpenCode depende da configuração escolhida pelo professor.

## Uso pelos alunos

1. Na pasta pronta, execute a loja:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

2. Abra [a loja](http://localhost:5000/) e [o painel](http://localhost:5000/painel).
3. Em outro terminal, execute o cliente de observação:

   ```powershell
   .\.venv\Scripts\python.exe cliente_mcp.py
   ```

4. Abra o OpenCode **na pasta do pacote**, com o `opencode.json` gerado na preparação:

   ```powershell
   opencode mcp list
   opencode
   ```

5. Faça perguntas, confira o painel, registre uma venda fictícia e repita as consultas.

O cliente Python inicia o servidor MCP automaticamente por **stdio** e chama as ferramentas diretamente. Ele não contém uma LLM. O OpenCode usa o mesmo servidor com o modelo configurado para escolher ferramentas a partir das perguntas.

O site Flask atende por HTTP na porta 5000. O servidor MCP é outro processo e acessa o **mesmo arquivo SQLite**. O MCP não depende de acessar as páginas HTML nem exige que o Flask esteja rodando para consultar o banco.

## Ferramentas disponíveis

| Tool | Argumentos | Resultado |
|---|---|---|
| `listar_produtos` | `categoria` opcional | Produtos, categorias e preços atuais |
| `produtos_mais_vendidos` | `limite=5`, `horas=168` | Ranking por unidades, receita e período |
| `valor_medio` | `horas=24` | Ticket médio, preço médio do catálogo e média por unidade vendida |
| `vendas_ultimas_24h` | nenhum | Quantidade de pedidos, unidades, receita, ticket e até dez pedidos recentes |

Ranking aceita de 1 a 20 posições. O período configurável vai de 1 a 8760 horas. O desempate do ranking usa receita e ID do produto. As tools devolvem início e fim da janela em UTC, com moeda em reais e alguns totais também em centavos.

## Perguntas prontas

> Use o MCP loja para listar os 5 produtos mais vendidos nos últimos 7 dias, por unidades. Mostre nome e quantidade.

> Use o MCP loja: qual foi o ticket médio nas últimas 24 horas? Qual é o preço médio atual do catálogo? Explique a diferença.

> Use o MCP loja para informar o número de pedidos, as unidades vendidas e a receita fictícia das últimas 24 horas.

> Acabei de registrar uma venda fictícia. Consulte novamente o MCP loja e compare com os números que você informou antes.

## Definições que devem aparecer nas respostas

- **Mais vendidos:** soma de unidades por produto no período, não quantidade de pedidos nem faturamento.
- **Receita fictícia:** soma dos totais dos pedidos no período.
- **Ticket médio:** receita do período dividida pelo número de pedidos.
- **Preço médio do catálogo:** média simples dos preços atuais dos produtos, sem ponderar as vendas.
- **Preço médio por unidade vendida:** receita dos itens do período dividida pelas unidades vendidas.
- **Últimas 24 horas:** janela móvel até o momento da consulta, não apenas o dia de hoje.

Sem pedidos, a receita e as unidades são zero, o ranking fica vazio e as médias de vendas retornam `null`. O preço médio do catálogo continua disponível. O painel apresenta datas no horário local do navegador.

## Atividade final: antes e depois

1. Consulte vendas de 24h e ranking de 7 dias. Anote os valores.
2. No carrinho, adicione duas unidades de um único produto e clique em **Registrar venda fictícia**.
3. Atualize o painel e repita as consultas MCP.
4. Confira: pedidos +1, unidades +2 e receita +2 vezes o preço do produto. O ticket médio deve corresponder à nova divisão. O preço médio do catálogo permanece igual.

Faça a comparação sem outras vendas no intervalo e sem registros cruzando o limite da janela. Para duplas independentes, entregue uma cópia local do banco a cada uma. **Simular 5 vendas** no painel gera mais pedidos fictícios para exploração livre.

## Arquivos do pacote

| Arquivo | Papel |
|---|---|
| `app.py`, `templates/`, `static/` | Site pronto, fora do escopo de desenvolvimento da aula |
| `banco.py` | Esquema, carga fictícia e registro de pedidos |
| `dados/loja.sqlite3` | Banco de referência pronto |
| `consultas.py` | Mesmos cálculos usados pelo painel e pelo MCP |
| `servidor_mcp.py` | Referência completa de quatro tools MCP |
| `cliente_mcp.py` | Chamadas diretas ao protocolo, sem LLM |
| `configurar_opencode.py` | Gera configuração local com caminhos absolutos |
| `requirements.txt`, `constraints_testadas.txt` | Versões verificadas para o ambiente |
| `iniciar_loja.bat` | Atalho de execução no Windows após a preparação |

## Dúvidas de execução

- **Porta ocupada:** encerre outra cópia da loja ou ajuste a porta em `app.py`.
- **Métricas diferentes:** confira os argumentos, os horários da consulta e se todos usam `dados/loja.sqlite3`. A variável de ambiente `LOJA_DB` permite outra base.
- **Sem vendas recentes:** use **Simular 5 vendas**, ou prepare as datas antes do encontro com `banco.py --atualizar-datas`.
- **Servidor MCP não aparece:** execute `configurar_opencode.py` com o Python da `.venv`, na pasta extraída, e reinicie o OpenCode. Se mover o pacote, gere a configuração novamente.
- **Faltam dependências:** repita a instalação dentro do ambiente virtual usando os arquivos de versões.
- **Página pede recarga:** recarregue após reiniciar o Flask, pois a sessão da demonstração muda no reinício.

## Versões e referências

Referência testada: Python 3.12, Flask 3.1.3 e SDK oficial MCP 1.28.1. O servidor usa `FastMCP`, da linha 1.x. Não substitua pela API 2.x sem adaptar os exemplos.

- [Flask: instalação](https://flask.palletsprojects.com/en/stable/installation/).
- [SDK oficial MCP, linha 1.x](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x).
- [OpenCode: configuração de servidores MCP](https://opencode.ai/docs/mcp-servers/).

Este pacote é um laboratório local de ensino. A aplicação usa `127.0.0.1`, dados fictícios e nenhuma integração de pagamento.
