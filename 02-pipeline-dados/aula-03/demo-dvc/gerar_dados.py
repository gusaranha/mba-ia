"""
Gerador de dados sintéticos para demo do DVC.
"""
import pandas as pd
import numpy as np
from pathlib import Path

def gerar_transacoes(n: int, seed: int) -> pd.DataFrame:
    """Gera transações com padrão de fraude detectável."""
    np.random.seed(seed)
    
    valor = np.random.exponential(500, n)
    hora = np.random.randint(0, 24, n)
    dia_semana = np.random.randint(0, 7, n)
    categoria = np.random.choice(['A', 'B', 'C', 'D'], n)
    
    # Fraude: valor alto + horário noturno + categoria D
    score = np.zeros(n)
    score += (valor > 800) * 0.4
    score += ((hora >= 22) | (hora <= 5)) * 0.3
    score += (categoria == 'D') * 0.2
    score += 0.02
    is_fraude = (np.random.random(n) < score).astype(int)
    
    return pd.DataFrame({
        'valor': valor,
        'hora': hora,
        'dia_semana': dia_semana,
        'categoria': categoria,
        'is_fraude': is_fraude
    })

if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)
    
    print("Gerando dados...")
    
    # Dados principais (v1)
    dados = gerar_transacoes(150000, seed=42)
    dados.to_csv("data/transacoes.csv", index=False)
    print(f"✓ data/transacoes.csv ({len(dados):,} linhas)")
    
    # Dados adicionais (para v2)
    novembro = gerar_transacoes(50000, seed=99)
    novembro.to_csv("data/novembro.csv", index=False)
    print(f"✓ data/novembro.csv ({len(novembro):,} linhas)")
    
    print("\nPronto!")
