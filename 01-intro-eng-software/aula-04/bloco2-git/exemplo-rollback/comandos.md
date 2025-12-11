# Roteiro: Rollback em Ação

## 🎬 Cenário

É segunda-feira, 14h. Você acabou de fazer deploy da versão 1.1 da API.

**📞 O telefone toca:** "A API está fora do ar! Todas as transações estão falhando!"

**Sua missão:** Reverter para a versão estável em menos de 1 minuto.

---

## 📋 Passo a Passo

### **1. Ver Histórico de Commits**

```bash
git log --oneline
```

**Resultado esperado:**
```
f9d8e7g feat: Adicionar normalização (v1.1) ← Commit problemático
a1b2c3d feat: Versão 1.0 estável
9f8e7d6 feat: Health check
```

---

### **2. Identificar o Commit Problemático**

O último commit (`f9d8e7g`) introduziu o bug. Você precisa reverter ele.

---

### **3. Reverter o Commit (Salvando a Produção)**

```bash
git revert f9d8e7g --no-edit
```

**O que acontece:**
- Git cria um **novo commit** que desfaz as mudanças do commit `f9d8e7g`
- O histórico é **preservado** (não apagamos nada)
- A API volta ao estado da versão 1.0

---

### **4. Verificar que o Bug Foi Removido**

```bash
cat main.py | grep "1 / 0"
```

**Resultado esperado:**
```
(nenhum resultado - o bug foi removido!)
```

---

### **5. Verificar Novo Histórico**

```bash
git log --oneline
```

**Resultado esperado:**
```
3c4d5e6 Revert "feat: Adicionar normalização (v1.1)" ← Novo commit de reversão
f9d8e7g feat: Adicionar normalização (v1.1) ← Commit problemático (preservado)
a1b2c3d feat: Versão 1.0 estável
9f8e7d6 feat: Health check
```

---

### **6. Testar API Restaurada**

```bash
uvicorn main:app --reload
```

Abra o navegador em: `http://localhost:8000/docs`

Envie um POST para `/analisar`:
```json
{
  "valor": 15000,
  "hora_do_dia": 14,
  "distancia_ultima_compra_km": 10,
  "numero_transacoes_hoje": 2,
  "idade_conta_dias": 180
}
```

**Resultado esperado:**
```json
{
  "fraude": true,
  "confianca": 0.95,
  "valor_processado": 15000.0,
  "motivo": "Valor acima do threshold de R$ 10.000"
}
```

✅ **API funcionando novamente!**

---

## 🎯 O Que Você Aprendeu

### **Por Que `git revert` e Não `git reset`?**

| Comando | O Que Faz | Quando Usar |
|---------|-----------|-------------|
| `git revert` | Cria novo commit que desfaz mudanças | ✅ **Produção** (preserva histórico) |
| `git reset` | Apaga commits do histórico | ⚠️ Apenas local (reescreve história) |

### **Princípios de Recuperação de Desastre**

1. **Velocidade**: Reverter em < 1 minuto é mais importante que diagnosticar
2. **Segurança**: Histórico preservado permite análise posterior
3. **Rastreabilidade**: Git nos diz exatamente o que mudou e quando

---

## 🔍 Comandos Extras (Investigação)

### **Quem Mudou Cada Linha?**
```bash
git blame main.py
```

**Resultado:**
```
f9d8e7g  (João Silva   2024-11-13)  resultado_normalizacao = 1 / 0
```

Agora você sabe quem falar para evitar isso no futuro!

---

### **Ver Diferenças Entre Versões**
```bash
git diff a1b2c3d f9d8e7g
```

Mostra exatamente o que foi adicionado/removido entre versões.

---

## 💡 Lições de Produção

1. **Sempre tenha um plano de rollback**: Antes de qualquer deploy
2. **Testes deveriam ter pegado isso**: Próximos blocos!
3. **Pull Requests evitam commits diretos**: Governança
4. **Git é sua rede de segurança**: Sem ele, você estaria perdido

---

## 🚨 Situação Real

**Tempo de recuperação:**
- ❌ Sem Git: 30+ minutos (procurar backup, re-deploy manual)
- ✅ Com Git: < 1 minuto (`git revert` + deploy)

**Custo do downtime:**
- E-commerce: R$ 10.000/minuto
- Fintech: R$ 50.000/minuto

**Git literalmente salva milhões.**

---

## 📚 Próximos Passos

Agora que você sabe **reverter** problemas, no **Bloco 3** você aprenderá a:
- **Diagnosticar** por que o bug aconteceu (Debug + Logs)
- **Prevenir** que ele volte (Bloco 4: Testes)
