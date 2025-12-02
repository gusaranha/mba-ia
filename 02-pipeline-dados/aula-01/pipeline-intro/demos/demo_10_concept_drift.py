"""
Demo 10: Simulando concept drift
Objetivo: Mostrar degradação de performance com tempo
"""

import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
import os

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

print("=" * 50)
print("SIMULANDO CONCEPT DRIFT")
print("=" * 50)
print()

# Carregar modelo treinado
print("Carregando modelo treinado...")
with open(os.path.join(MODEL_DIR, 'modelo_fraude.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(MODEL_DIR, 'label_encoder.pkl'), 'rb') as f:
    le = pickle.load(f)

print("✅ Modelo carregado")
print()

# Simular dados de 6 meses
meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho']
meses_labels = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']
f1_scores = []

for mes, mes_label in zip(meses, meses_labels):
    print(f"Avaliando {mes_label}...")
    
    # Carregar dados do mês
    arquivo = f'transacoes_{mes}.csv'
    df_mes = pd.read_csv(os.path.join(DATA_DIR, arquivo))
    
    # Preparar features
    df_mes['categoria_cod'] = le.transform(df_mes['categoria'])
    X_mes = df_mes[['valor', 'hora', 'categoria_cod']]
    y_mes = df_mes['is_fraud']
    
    # Fazer predições
    y_pred = model.predict(X_mes)
    
    # Calcular F1
    f1 = f1_score(y_mes, y_pred)
    f1_scores.append(f1)
    
    status = "✅ OK" if f1 >= 0.75 else "🚨 ALERTA"
    print(f"  F1-Score: {f1:.4f} {status}")
    print()

# Visualizar degradação
print("=" * 50)
print("EVOLUÇÃO DA PERFORMANCE")
print("=" * 50)
print()

plt.figure(figsize=(10, 6))
plt.plot(meses_labels, f1_scores, marker='o', linewidth=2, markersize=10, color='#2E86AB')
plt.axhline(y=0.75, color='red', linestyle='--', linewidth=2, label='Threshold Mínimo (75%)')
plt.xlabel('Mês', fontsize=12)
plt.ylabel('F1-Score', fontsize=12)
plt.title('Degradação de Performance ao Longo do Tempo (Concept Drift)', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.ylim(0.5, 1.0)

# Adicionar valores nos pontos
for i, (mes, f1) in enumerate(zip(meses_labels, f1_scores)):
    plt.text(i, f1 + 0.02, f'{f1:.3f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('concept_drift.png', dpi=150, bbox_inches='tight')
print("✅ Gráfico salvo em 'concept_drift.png'")
plt.show()

# Análise
print("\nAnálise mês a mês:")
for mes, f1 in zip(meses_labels, f1_scores):
    status = "✅ OK" if f1 >= 0.75 else "🚨 ALERTA"
    print(f"  {mes:10s}: {f1:.4f} {status}")
print()

# Recomendação
if min(f1_scores) < 0.75:
    print("=" * 50)
    print("🚨 RECOMENDAÇÃO: RETREINAR MODELO")
    print("=" * 50)
    print("Performance caiu abaixo do threshold mínimo.")
    print("Ações sugeridas:")
    print("  1. Retreinar com dados recentes (últimos 3 meses)")
    print("  2. Investigar novos padrões de fraude")
    print("  3. Adicionar features relevantes")
    print("  4. Configurar alertas automáticos")
