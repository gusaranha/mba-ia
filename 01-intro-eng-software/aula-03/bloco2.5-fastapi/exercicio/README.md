# Exercício - API de Usuários

## Objetivo

Criar API simples com validação Pydantic seguindo os TODOs em `main.py`

## Tarefas

1. ✅ Criar classe `Usuario` com validações
2. ✅ Criar endpoint raiz GET "/"
3. ✅ Criar endpoint POST "/usuarios"
4. ✅ Criar endpoint GET "/usuarios/{usuario_id}"
5. ✅ Testar casos válidos e inválidos

## Executar
```bash
uvicorn main:app --reload
```

## Casos de Teste

**Válido:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "idade": 25,
  "ativo": true
}
```

**Inválidos para testar:**

1. Nome curto demais
2. Idade menor que 18
3. Idade maior que 100
4. Campos faltando

## Dicas

- Use `Field(...)` para campos obrigatórios
- Use `Field(..., min_length=X)` para strings
- Use `Field(..., ge=X, le=Y)` para números
- Consulte `../exemplo-simples/` se travar
