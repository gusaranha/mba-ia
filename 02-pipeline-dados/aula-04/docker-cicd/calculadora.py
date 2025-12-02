"""
Calculadora de Score de Crédito - Versão Super Simples

Entrada: renda, idade, dívidas
Saída: score de crédito (0-100)
"""

def calcular_score(renda: float, idade: int, dividas: float) -> int:
    """
    Calcula score de crédito baseado em regras simples.
    
    Returns:
        Score entre 0 e 100
    """
    score = 50  # Base
    
    # Renda contribui positivamente
    if renda > 5000:
        score += 20
    elif renda > 3000:
        score += 10
    
    # Idade contribui (experiência)
    if idade > 30:
        score += 15
    elif idade > 25:
        score += 10
    
    # Dívidas contribuem negativamente
    if dividas > 10000:
        score -= 30
    elif dividas > 5000:
        score -= 15
    
    # Garantir entre 0-100
    score = max(0, min(100, score))
    
    return score


if __name__ == "__main__":
    print("🏦 Calculadora de Score de Crédito")
    print("=" * 40)
    
    # Exemplos
    exemplos = [
        {"renda": 6000, "idade": 35, "dividas": 2000, "esperado": "Alto"},
        {"renda": 2000, "idade": 22, "dividas": 8000, "esperado": "Baixo"},
        {"renda": 4000, "idade": 28, "dividas": 4000, "esperado": "Médio"},
    ]
    
    for ex in exemplos:
        score = calcular_score(ex["renda"], ex["idade"], ex["dividas"])
        print(f"\nRenda: R$ {ex['renda']:.2f}")
        print(f"Idade: {ex['idade']} anos")
        print(f"Dívidas: R$ {ex['dividas']:.2f}")
        print(f"Score: {score} ({ex['esperado']})")
