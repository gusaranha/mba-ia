"""
Validador de Dados - Verifica se dados de entrada são válidos
"""
import pandas as pd
import pandera as pa
from pandera import Column, Check

# Schema: regras que os dados devem seguir
ClienteSchema = pa.DataFrameSchema({
    "renda": Column(float, [
        Check.ge(0, error="Renda não pode ser negativa"),
        Check.le(100000, error="Renda muito alta, verificar"),
    ]),
    "idade": Column(int, [
        Check.ge(18, error="Idade mínima: 18 anos"),
        Check.le(100, error="Idade inválida"),
    ]),
    "dividas": Column(float, [
        Check.ge(0, error="Dívidas não podem ser negativas"),
    ]),
})


def validar_dados(dados: pd.DataFrame) -> bool:
    """
    Valida dados de clientes.
    
    Returns:
        True se válido, levanta erro se inválido
    """
    ClienteSchema.validate(dados)
    return True


if __name__ == "__main__":
    print("✅ Testando validação...")
    
    # Dados VÁLIDOS
    dados_validos = pd.DataFrame({
        "renda": [3000.0, 5000.0, 8000.0],
        "idade": [25, 30, 45],
        "dividas": [1000.0, 5000.0, 2000.0],
    })
    
    try:
        validar_dados(dados_validos)
        print("✅ Dados válidos passaram!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Dados INVÁLIDOS (idade < 18)
    dados_invalidos = pd.DataFrame({
        "renda": [3000.0],
        "idade": [16],  # ❌ Menor de idade!
        "dividas": [1000.0],
    })
    
    try:
        validar_dados(dados_invalidos)
        print("✅ Dados inválidos passaram (ERRO!)")
    except Exception as e:
        print(f"❌ Dados inválidos rejeitados (correto!): Idade mínima: 18 anos")
