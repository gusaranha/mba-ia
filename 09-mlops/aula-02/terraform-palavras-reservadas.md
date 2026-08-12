# Palavras Reservadas do Terraform/HCL — Guia de Referência

## Antes de tudo: 4 camadas de vocabulário diferentes

A confusão que você descreveu (`source`, `local`, `aws`...) existe porque tem 4 "dicionários" diferentes convivendo no mesmo arquivo `.tf`, e visualmente eles são idênticos — texto minúsculo, sem aspas às vezes. Separando pela sua própria dúvida:

| Trecho | Camada | É "reservado"? |
|---|---|---|
| `provider` (a palavra em si) | Terraform core — nome de bloco de topo | **Sim** |
| `"azurerm"` logo depois de `provider` | um alias local — você escolhe, por convenção bate com o nome do provider | **Não** |
| `source` dentro de `required_providers` | atributo esperado por aquele bloco específico | Sim, mas só *naquele contexto* |
| `"hashicorp/azurerm"` (o valor) | endereço do provider no Registry — é um dado, não linguagem | **Não** |
| `local_file` em `resource "local_file" "x"` | nome de *tipo* de resource — vocabulário do provider `local` | **Não** (não é reservado pelo Terraform core) |
| o prefixo `local_`, `aws_`, `azurerm_` | convenção de nomenclatura de cada provider | **Não** |

Ou seja: o único motivo de `"azurerm"` aparecer tanto é *coincidência de convenção* — o alias que você escolhe pro provider geralmente recebe o mesmo nome do provider em si, mas isso é hábito, não regra da linguagem.

Com isso separado, aqui vai a lista real, organizada pelas suas 6 áreas.

---

## 1. Fundamentos

Aqui, sinceramente, quase não existem palavras reservadas — a maior parte do que vimos nessa área (IaC, Declarativo, Idempotência) é **vocabulário conceitual do campo**, não sintaxe. As únicas palavras que a HCL de fato reserva na camada de expressão são:

| Palavra | Explicação |
|---|---|
| `true` | literal booleano — não pode ser usado como nome de variável com outro sentido |
| `false` | literal booleano |
| `null` | valor "ausente" — usado pra dizer "esse argumento não tem valor" |

Isso é literalmente tudo que a gramática da HCL reserva no nível de expressão. Tudo mais que parece palavra-chave vem das camadas abaixo.

---

## 2. Fluxo de Trabalho

**Nenhuma dessas é palavra reservada da linguagem HCL** — são subcomandos do binário `terraform`, um dicionário totalmente separado (você nunca digita `init` *dentro* de um arquivo `.tf`).

| Comando | Explicação |
|---|---|
| `init` | baixa os providers/módulos declarados |
| `validate` | checa sintaxe e consistência interna |
| `fmt` | formata o código no padrão oficial |
| `plan` | calcula e mostra as mudanças, sem aplicar |
| `apply` | executa as mudanças de verdade |
| `destroy` | remove tudo que está no state |
| `refresh` | atualiza o state comparando com a nuvem |
| `import` | traz um recurso existente pro controle do Terraform |
| `state` | subcomandos pra inspecionar/editar o state (`list`, `show`, `mv`, `rm`) |
| `output` | imprime os valores declarados em blocos `output` |
| `console` | abre o REPL interativo |
| `workspace` | gerencia workspaces |
| `graph` | gera o grafo de dependências |
| `taint` / `-replace` | força a recriação de um recurso específico |

---

## 3. Blocos da Linguagem

É aqui que moram as palavras "reservadas" de verdade — mas reservadas *pelo Terraform*, não pela gramática genérica da HCL (a distinção do Apêndice A do manual em BNF: isso é regra de *validação semântica* da ferramenta, não da gramática formal).

### Blocos de topo
| Palavra | Explicação |
|---|---|
| `terraform` | configura a própria ferramenta: versão exigida, providers, backend |
| `provider` | configura uma instância de um provider |
| `resource` | declara algo que será criado/gerenciado |
| `data` | lê algo que já existe, sem criar |
| `variable` | declara uma entrada parametrizável |
| `output` | expõe um valor após o apply |
| `locals` | define valores locais reutilizáveis (nota: bloco no **plural**) |
| `module` | chama um módulo reutilizável |

### Prefixos de referência (o "espelho" de cada bloco acima)
Ponto de confusão clássico — repare que nem todos batem no singular/plural com o bloco que os originou:

| Prefixo | Referencia | Exemplo |
|---|---|---|
| `var.` | um `variable` | `var.regiao` |
| `local.` | um `locals` (⚠️ **singular**, mesmo o bloco sendo `locals`) | `local.nome_padrao` |
| `module.` | o output de um `module` | `module.vpc.id` |
| `data.` | um `data` | `data.aws_ami.ubuntu.id` |
| `path.` | caminhos especiais (não vem de bloco nenhum) | `path.module`, `path.root` |

### Meta-argumentos (reservados só dentro de `resource`/`data`/`module`)
| Palavra | Explicação |
|---|---|
| `count` | cria N instâncias, indexadas por número |
| `for_each` | cria uma instância por item de um mapa/set |
| `depends_on` | força uma dependência explícita |
| `provider` | escolhe qual configuração de provider usar (mesmo nome do bloco de topo, mas aqui é meta-argumento) |
| `lifecycle` | bloco aninhado com regras especiais (veja abaixo) |

### Dentro de `lifecycle { }`
| Palavra | Explicação |
|---|---|
| `create_before_destroy` | cria o novo antes de destruir o antigo |
| `prevent_destroy` | bloqueia `destroy` acidental |
| `ignore_changes` | ignora mudanças em atributos específicos |
| `precondition` / `postcondition` | validações antes/depois da operação |
| `replace_triggered_by` | força recriação quando outro recurso muda |

### Outros blocos especiais
| Palavra | Explicação |
|---|---|
| `dynamic` | gera blocos aninhados repetidos dinamicamente |
| `provisioner` | executa script após criar o recurso (uso desencorajado) |
| `connection` | define SSH/WinRM pra um provisioner |

---

## 4. Estado

| Palavra | Explicação | É reservado? |
|---|---|---|
| `backend` | bloco que define onde o state fica guardado | Sim — nome de bloco |
| `cloud` | alternativa ao `backend`, pra integrar com HCP Terraform | Sim |
| tipos de backend: `local`, `remote`, `azurerm`, `s3`, `gcs`, `consul`, `pg`, `http`... | o *tipo* de backend que você escolhe | **Sim, mas é uma lista fechada** |

Ponto sutil que vale destacar em aula: diferente do nome de um *provider* (que é aberto — qualquer um pode publicar um novo no Registry), os tipos de **backend** são um conjunto fixo, compilado dentro do próprio binário do Terraform. Você não pode inventar `backend "meu-backend-customizado"` — só pode usar um dos que o Terraform já suporta nativamente.

---

## 5. Multi-Cloud

Essa é a área com a resposta mais direta pra sua pergunta original: **nada aqui é palavra reservada.**

| Trecho | O que realmente é |
|---|---|
| `"azurerm"`, `"aws"`, `"google"` (label do provider) | alias local — por convenção, igual ao nome do provider, mas trocável |
| `azurerm_`, `aws_`, `google_` (prefixo dos tipos de resource) | convenção de nomenclatura — cada provider decide a própria |
| `"hashicorp/azurerm"` (o `source`) | endereço no Terraform Registry — um dado, como uma URL |
| nomes de região (`"us-east-1"`, `"Brazil South"`) | valores de string — cada provider define seu próprio formato |

Se um aluno perguntar "por que `aws_s3_bucket` e não `s3_bucket`?" — a resposta correta é "porque o time que mantém o provider `aws` decidiu essa convenção", não "porque é regra do Terraform". Provider nenhum é obrigado a prefixar assim (a maioria segue por convenção da comunidade, não por exigência técnica).

---

## 6. Boas Práticas

| Palavra/Símbolo | Explicação | É reservado? |
|---|---|---|
| `sensitive` | atributo que esconde o valor no output do terminal | Sim, mas só dentro de `variable`/`output` |
| `count.index` | índice da iteração atual, disponível só dentro de um bloco com `count` | Sim, contextual |
| `each.key` / `each.value` | chave/valor da iteração atual, só dentro de um bloco com `for_each` | Sim, contextual |
| `~>`, `>=`, `<=`, `!=` | operadores de *version constraint* — uma mini-linguagem própria dentro do argumento `version` | Sim, mas é uma sintaxe à parte, não a HCL geral |
| `.terraform.lock.hcl` | nome de arquivo fixo que o Terraform procura automaticamente | É convenção de nome de arquivo, não palavra de código |

---

## Tabela-resumo pra consulta rápida

| Categoria de vocabulário | Exemplos | Quem define |
|---|---|---|
| Literais da HCL | `true`, `false`, `null` | a gramática da linguagem |
| Blocos de topo do Terraform | `resource`, `provider`, `variable`... | o Terraform core |
| Meta-argumentos | `count`, `for_each`, `lifecycle` | o Terraform core |
| Tipos de backend | `azurerm`, `s3`, `local`... | o Terraform core (lista fechada) |
| Subcomandos da CLI | `init`, `plan`, `apply` | o binário `terraform` (namespace à parte) |
| Nomes de provider | `aws`, `azurerm`, `google`, `docker`... | o Registry (aberto, qualquer um publica) |
| Tipos de resource/data | `aws_s3_bucket`, `azurerm_storage_account` | cada provider individualmente |
| Nomes de resource/variável/módulo | `rg`, `app`, `minha_vpc` | **você** |

A régua mental pra qualquer palavra estranha num código Terraform: pergunte "isso é do Terraform, ou é de um provider, ou fui eu (ou quem escreveu o código) que inventei esse nome?" — nessa ordem, e a resposta quase sempre aparece.
