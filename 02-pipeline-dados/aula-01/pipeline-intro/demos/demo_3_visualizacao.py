"""
Demo 3: Visualização de Dados
Objetivo: Criar gráficos para entender padrões nas transações
"""

import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('../data/transacoes.csv')

# ===== CRIAR FIGURA COM SUBPLOTS =====
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
# 2, 2 = grid de 2 linhas x 2 colunas (4 gráficos)
# figsize=(12, 8) = largura 12 polegadas, altura 8 polegadas


# ===== GRÁFICO 1: HISTOGRAMA DE VALORES =====
axes[0, 0].hist(df['valor'], bins=50, edgecolor='black')
# bins=50 = divide os dados em 50 intervalos (barras)
# edgecolor='black' = borda preta nas barras

axes[0, 0].set_title('Distribuição de Valores')
axes[0, 0].set_xlabel('Valor (R$)')
axes[0, 0].set_ylabel('Frequência')


# ===== GRÁFICO 2: FRAUDES VS LEGÍTIMAS =====
df['is_fraud'].value_counts().plot(kind='bar', ax=axes[0, 1])
# kind='bar' = gráfico de barras verticais
# ax=axes[0, 1] = posição: linha 0, coluna 1

axes[0, 1].set_title('Fraudes vs Legítimas')
axes[0, 1].set_xlabel('Tipo (0=Legítima, 1=Fraude)')
axes[0, 1].set_ylabel('Quantidade')
axes[0, 1].set_xticklabels(['Legítima', 'Fraude'], rotation=0)
# set_xticklabels = renomeia os rótulos do eixo X
# rotation=0 = sem rotação (horizontal)


# ===== GRÁFICO 3: TRANSAÇÕES POR HORA =====
df['hora'].value_counts().sort_index().plot(kind='line', ax=axes[1, 0], marker='o')
# sort_index() = ordena por hora (0 a 23)
# kind='line' = gráfico de linha
# marker='o' = marcador circular em cada ponto

axes[1, 0].set_title('Transações por Hora do Dia')
axes[1, 0].set_xlabel('Hora')
axes[1, 0].set_ylabel('Quantidade')
axes[1, 0].grid(True, alpha=0.3)
# grid=True = mostra linhas de grade
# alpha=0.3 = transparência 30% (0=invisível, 1=opaco)


# ===== GRÁFICO 4: VALOR MÉDIO POR CATEGORIA =====
df.groupby('categoria')['valor'].mean().plot(kind='bar', ax=axes[1, 1])
# groupby('categoria') = agrupa por categoria
# ['valor'].mean() = calcula média dos valores

axes[1, 1].set_title('Valor Médio por Categoria')
axes[1, 1].set_xlabel('Categoria')
axes[1, 1].set_ylabel('Valor Médio (R$)')
axes[1, 1].set_xticklabels(['A', 'B', 'C', 'D'], rotation=0)


# ===== AJUSTAR LAYOUT E SALVAR =====
plt.tight_layout()
# ajusta automaticamente os espaçamentos entre gráficos

plt.savefig('exploracao.png', dpi=150, bbox_inches='tight')
# dpi=150 = resolução 150 pontos por polegada (qualidade)
# bbox_inches='tight' = remove espaços em branco extras

plt.show()
# exibe a figura na tela

print("\n✓ Gráfico salvo como 'exploracao.png'")