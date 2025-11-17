# API de Servidores e Tarefas

Este projeto implementa uma API REST, usando FastAPI, para gerenciar **servidores** (colaboradores) e suas **tarefas**, bem como o cálculo de carga de trabalho (horas disponíveis e porcentagem de ocupação).

A API expõe endpoints para:

- CRUD básico de **Servidores**
- CRUD básico de **Tarefas**
- Consulta da **distribuição de tarefas de um servidor**, incluindo:
  - horas totais designadas
  - horas ainda disponíveis
  - porcentagem de ocupação da carga horária

---

## Modelos de Dados (Schemas)

### Servidor

Representa um colaborador que pode receber tarefas.

- `ServidorIn`
  - `nome` (str): nome do servidor (mín. 5, máx. 100 caracteres).
  - `carga_horaria` (int): carga semanal de trabalho (entre 10 e 80 horas, por exemplo).

- `ServidorOut` (herda de `ServidorIn`)
  - `id` (int): identificador único do servidor.

- `ServidorTarefas`
  - `servidor` (`ServidorOut`): dados do servidor.
  - `tarefas_designadas` (lista de `TarefaOut`): lista de tarefas atribuídas ao servidor.
  - `horas_disponiveis` (int): carga horária ainda disponível (não negativa).
  - `porcentagem_ocupacao` (int): percentual da carga horária já utilizada (0 a 100).

### Tarefa

Representa uma atividade atribuída a um servidor.

- `TarefaIn`
  - `descricao` (str): descrição da tarefa.
  - `horas_execucao` (int): número de horas estimadas para execução.
  - `responsavel_id` (int): id do servidor responsável.

- `TarefaOut` (herda de `TarefaIn`)
  - `id` (int): identificador único da tarefa.

*(Os schemas de tarefa seguem esse formato, com base no uso nos endpoints e testes.)*

---

## Endpoints

Todos os endpoints seguem o padrão base da API, por exemplo: `/api/v1`.

### Servidores

Prefixo: `/servidores`

- `GET /servidores`
  - Retorna uma lista de `ServidorOut`.
  - Usado para listar todos os servidores cadastrados.

- `GET /servidores/{servidor_id}`
  - Retorna um `ServidorOut` com o `id` informado.
  - **404** se o servidor não existir.

- `POST /servidores`
  - Corpo (`JSON`): `ServidorIn`.
  - Retorna `ServidorOut` com **status 201**.
  - Regras de validação:
    - `carga_horaria` deve ser maior que zero;
    - caso contrário, é retornado um erro de requisição inválida (400).

- `DELETE /servidores/{servidor_id}`
  - Remove o servidor com o `id` informado.
  - **204** em caso de sucesso.
  - **404** se o servidor não existir.

- `GET /servidores/{servidor_id}/tarefas`
  - Retorna um `ServidorTarefas` com:
    - dados do servidor
    - lista de tarefas atribuídas
    - `horas_disponiveis`
    - `porcentagem_ocupacao`
  - Regras:
    - **404** se o servidor não existir.
    - **400** se a carga horária do servidor for inválida (0).
    - `horas_disponiveis` é calculado como:
      - `carga_horaria - soma(horas_execucao das tarefas)`
    - `porcentagem_ocupacao` é:
      - `horas_tarefas / carga_horaria * 100`
    - Se as horas das tarefas extrapolarem a carga:
      - `horas_disponiveis = 0`
      - `porcentagem_ocupacao = 100`

### Tarefas

Prefixo: `/tarefas`

- `GET /tarefas`
  - Retorna lista de `TarefaIn`/`TarefaOut` cadastradas.

- `GET /tarefas/{tarefa_id}`
  - Retorna `TarefaOut` da tarefa informada.
  - **404** se a tarefa não existir.

- `POST /tarefas`
  - Corpo (`JSON`): `TarefaIn`.
  - Retorna `TarefaOut` com **status 201**.
  - Atribui a tarefa ao servidor identificado por `responsavel_id`.

- `DELETE /tarefas/{tarefa_id}`
  - Remove a tarefa informada.
  - **204** em caso de sucesso.
  - **404** se a tarefa não existir.

---

## Regras de Negócio Principais

- Um servidor possui:
  - Nome e carga horária cadastrados.
  - Carga horária não pode ser zero.
- As tarefas são sempre associadas a um servidor por meio de `responsavel_id`.
- O endpoint `/servidores/{servidor_id}/tarefas` consolida a visão de:
  - tarefas atribuídas
  - horas já comprometidas
  - capacidade livre e percentual de ocupação.

---

## Testes Automatizados

Há testes automatizados que validam o comportamento da API:

### Testes de Tarefas

- Criação de tarefa:
  - `POST /api/v1/tarefas` deve retornar **201** e os campos `id`, `descricao`, `horas_execucao`, `responsavel_id`.
- Listagem:
  - `GET /api/v1/tarefas` deve retornar **200** e uma lista (com pelo menos 1 tarefa após criação).
- Busca por id:
  - `GET /api/v1/tarefas/1` deve retornar **200** quando a tarefa existe.
  - `GET /api/v1/tarefas/999` deve retornar **404** para tarefa inexistente.
- Exclusão:
  - `DELETE /api/v1/tarefas/1` deve retornar **204**.

### Testes de Servidores

- Criação:
  - `POST /api/v1/servidores` cria um servidor e retorna **201** com `id`, `nome`, `carga_horaria`.
- Listagem:
  - `GET /api/v1/servidores` retorna **200** e uma lista com pelo menos 1 servidor.
- Busca:
  - `GET /api/v1/servidores/1` retorna **200** para servidor existente.
  - `GET /api/v1/servidores/999` retorna **404**.
- Exclusão:
  - `DELETE /api/v1/servidores/1` retorna **204**.
- Cálculo de tarefas e ocupação:
  - Cria-se um servidor com `carga_horaria = 10`.
  - Sem tarefas:
    - `horas_disponiveis = 10`
    - `porcentagem_ocupacao = 0`
  - Após tarefas de 2h, 3h e 7h, a API deve:
    - Atualizar corretamente `horas_disponiveis`
    - Atualizar corretamente `porcentagem_ocupacao`
    - Truncar a disponibilidade a 0 e a ocupação a 100% quando a soma das tarefas excede a carga horária.

---

## Como Executar

1. Certifique-se de ter Python 3.12 e um ambiente virtual configurado.
2. Instale as dependências do projeto (por exemplo, via `pip install -r requirements.txt`, se o arquivo existir).
3. Suba o servidor FastAPI com `uvicorn` (o módulo/objeto `app` pode variar conforme a estrutura, por exemplo):

   ```bash
   uvicorn src.api.main:app --reload
   ```

4. Acesse a documentação interativa (OpenAPI) em:

   - `http://localhost:8000/docs`
   - ou `http://localhost:8000/redoc`

5. Para rodar os testes (se `pytest` estiver instalado):

   ```bash
   pytest
   ```

---

## Objetivo Didático

Este projeto serve como exercício introdutório de:

- Modelagem de dados com Pydantic.
- Criação de rotas e tratamento de erros com FastAPI.
- Separação de camadas (rotas, repositórios, modelos).
- Escrita de testes automatizados de API com `TestClient`.
- Raciocínio sobre regras de negócio (gerenciamento de carga de trabalho).