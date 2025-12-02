"""
Testes - Verificam se calculadora funciona corretamente
"""
import pytest
from calculadora import calcular_score


def test_score_alto():
    """Pessoa com boa renda, idade e poucas dívidas = score alto"""
    score = calcular_score(renda=6000, idade=35, dividas=2000)
    assert score >= 70, f"Score deveria ser >= 70, mas foi {score}"


def test_score_baixo():
    """Pessoa com baixa renda, jovem e muitas dívidas = score baixo"""
    score = calcular_score(renda=2000, idade=22, dividas=8000)
    assert score <= 40, f"Score deveria ser <= 40, mas foi {score}"


def test_score_medio():
    """Pessoa com perfil médio = score médio"""
    score = calcular_score(renda=4000, idade=28, dividas=4000)
    assert 40 < score < 70, f"Score deveria estar entre 40-70, mas foi {score}"


def test_score_dentro_limites():
    """Score nunca pode ser < 0 ou > 100"""
    # Teste extremo negativo
    score_min = calcular_score(renda=0, idade=18, dividas=50000)
    assert 0 <= score_min <= 100
    
    # Teste extremo positivo
    score_max = calcular_score(renda=50000, idade=60, dividas=0)
    assert 0 <= score_max <= 100


if __name__ == "__main__":
    print("🧪 Rodando testes...")
    pytest.main([__file__, "-v"])
