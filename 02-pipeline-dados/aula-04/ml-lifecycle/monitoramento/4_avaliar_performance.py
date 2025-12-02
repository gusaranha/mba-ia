"""
4. AVALIAR PERFORMANCE EM PRODUÇÃO

Testa o modelo v1.0 (treinado em Outubro) com dados de Novembro.
Detecta degradação de performance (concept drift).
"""
import pickle
import json
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score
from pathlib import Path

print("📊 RELATÓRIO DE MONITORAMENTO - Novembro 2025")
print("=" * 60)

# Carregar modelo de produção
model_path = Path("../producao/models/producao.pkl")
metadata_path = Path("../producao/metadata.json")

if not model_path.exists():
    print("❌ Erro: Modelo de produção não encontrado")
    exit(1)

with open(model_path, "rb") as f:
    modelo = pickle.load(f)

with open(metadata_path, "r") as f:
    metadata = json.load(f)

# Carregar dados de Outubro (baseline) e Novembro (produção)
df_outubro = pd.read_csv("../dados/outubro_2025.csv")
df_novembro = pd.read_csv("../dados/novembro_2025.csv")

print(f"\n📅 Período de Análise")
print(f"   Treino: Outubro 2025 ({len(df_outubro)} transações, {df_outubro['is_fraud'].sum()/len(df_outubro)*100:.0f}% fraude)")
print(f"   Produção: Novembro 2025 ({len(df_novembro)} transações, {df_novembro['is_fraud'].sum()/len(df_novembro)*100:.0f}% fraude)")

print(f"\n🤖 Modelo em Produção")
print(f"   Versão: {metadata['versao']}")
print(f"   Deploy: {metadata['data_deploy']}")
print(f"   Algoritmo: {metadata['algoritmo']}")

# Avaliar em Outubro (baseline)
X_out = df_outubro[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y_out = df_outubro["is_fraud"]
y_pred_out = modelo.predict(X_out)

f1_out = f1_score(y_out, y_pred_out)
prec_out = precision_score(y_out, y_pred_out)
rec_out = recall_score(y_out, y_pred_out)

print(f"\n📈 MÉTRICAS - OUTUBRO (Baseline)")
print(f"   F1 Score:  {f1_out:.3f}  {'━' * int(f1_out * 20)} 100%")
print(f"   Precision: {prec_out:.3f}  {'━' * int(prec_out * 20)} {int(prec_out/f1_out*100):3d}%")
print(f"   Recall:    {rec_out:.3f}  {'━' * int(rec_out * 20)} {int(rec_out/f1_out*100):3d}%")

# Avaliar em Novembro (produção)
X_nov = df_novembro[["valor", "hora", "categoria_cod", "qtd_transacoes_24h"]]
y_nov = df_novembro["is_fraud"]
y_pred_nov = modelo.predict(X_nov)

f1_nov = f1_score(y_nov, y_pred_nov)
prec_nov = precision_score(y_nov, y_pred_nov)
rec_nov = recall_score(y_nov, y_pred_nov)

degradacao_f1 = ((f1_nov - f1_out) / f1_out) * 100
degradacao_prec = ((prec_nov - prec_out) / prec_out) * 100
degradacao_rec = ((rec_nov - rec_out) / rec_out) * 100

print(f"\n📉 MÉTRICAS - NOVEMBRO (Produção)")
barra_f1 = int(f1_nov * 20)
print(f"   F1 Score:  {f1_nov:.3f}  {'━' * barra_f1}{'░' * (20-barra_f1)}  {int(f1_nov/f1_out*100):3d}%  ⚠️  {degradacao_f1:+.1f}%")
barra_prec = int(prec_nov * 20)
print(f"   Precision: {prec_nov:.3f}  {'━' * barra_prec}{'░' * (20-barra_prec)}  {int(prec_nov/prec_out*100):3d}%  ⚠️  {degradacao_prec:+.1f}%")
barra_rec = int(rec_nov * 20)
print(f"   Recall:    {rec_nov:.3f}  {'━' * barra_rec}{'░' * (20-barra_rec)}  {int(rec_nov/rec_out*100):3d}%  ⚠️  {degradacao_rec:+.1f}%")

# Análise de alertas
print(f"\n🚨 ALERTAS DETECTADOS\n")

alerta_critico = abs(degradacao_f1) > 10

if alerta_critico:
    print(f"  1. DEGRADAÇÃO CRÍTICA")
    print(f"     F1 Score caiu {abs(degradacao_f1):.1f} pontos percentuais")
    print(f"     Limite: 10% | Atual: {abs(degradacao_f1):.1f}%")
    print(f"     Status: ⛔ CRÍTICO\n")
else:
    print(f"  1. Performance estável")
    print(f"     Degradação: {degradacao_f1:+.1f}% (limite: ±10%)")
    print(f"     Status: ✅ OK\n")

# Mudança na taxa de fraude
taxa_out = df_outubro['is_fraud'].sum() / len(df_outubro)
taxa_nov = df_novembro['is_fraud'].sum() / len(df_novembro)
mudanca_taxa = ((taxa_nov - taxa_out) / taxa_out) * 100

print(f"  2. MUDANÇA NO PADRÃO DE FRAUDES")
print(f"     Taxa Outubro: {taxa_out*100:.0f}%")
print(f"     Taxa Novembro: {taxa_nov*100:.0f}% ({mudanca_taxa:+.0f}%)\n")

# Análise de padrões
print(f"  3. NOVOS PADRÕES IDENTIFICADOS")
fraudes_nov = df_novembro[df_novembro['is_fraud'] == 1]
fraudes_out = df_outubro[df_outubro['is_fraud'] == 1]

valor_medio_out = fraudes_out['valor'].mean()
valor_medio_nov = fraudes_nov['valor'].mean()
mudanca_valor = ((valor_medio_nov - valor_medio_out) / valor_medio_out) * 100

print(f"     • Valores médios de fraude: R$ {valor_medio_out:.0f} → R$ {valor_medio_nov:.0f} ({mudanca_valor:+.0f}%)")

# Categorias novas
cats_nov = set(df_novembro['categoria'].unique())
cats_out = set(df_outubro['categoria'].unique())
novas_cats = cats_nov - cats_out

if novas_cats:
    print(f"     • Novas categorias detectadas: {', '.join(novas_cats)}")

# Horários
hora_media_out = fraudes_out['hora'].mean()
hora_media_nov = fraudes_nov['hora'].mean()
print(f"     • Horário médio fraudes: {hora_media_out:.0f}h → {hora_media_nov:.0f}h")

# Recomendação
print(f"\n💡 RECOMENDAÇÃO: {'RETREINAMENTO URGENTE' if alerta_critico else 'Monitorar'}")

if alerta_critico:
    print(f"\n   Ações sugeridas:")
    print(f"   1. Retreinar com dados Outubro + Novembro")
    print(f"   2. Ajustar para nova taxa de fraude ({taxa_nov*100:.0f}%)")
    print(f"   3. Incorporar novos padrões")
    print(f"   4. Promover novo modelo para produção")

print(f"\n" + "=" * 60)
print(f"👉 Próximo passo: Execute '../retreinamento/5_retreinar_modelo.py'")
