"""
Demonstração: Tratamento de erros
Mostra diferença entre código com e sem tratamento de erros
"""

import pandas as pd


# ============================================
# VERSÃO 1: Sem tratamento (código quebra)
# ============================================

def carregar_v1(caminho):
    """Carrega sem tratamento - pode quebrar"""
    df = pd.read_csv(caminho)
    return df


# ============================================
# VERSÃO 2: Com tratamento básico
# ============================================

def carregar_v2(caminho):
    """Carrega com tratamento de erro"""
    try:
        df = pd.read_csv(caminho)
        print(f"✅ Carregado: {len(df)} linhas")
        return df
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho}")
        return None


# ============================================
# VERSÃO 3: Com validações extras
# ============================================

def carregar_v3(caminho):
    """Carrega com tratamento e validações"""
    # Verificar se é CSV
    if not caminho.endswith('.csv'):
        print(f"❌ Arquivo deve ser CSV: {caminho}")
        return None
    
    try:
        df = pd.read_csv(caminho)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho}")
        return None
    
    # Verificar se não está vazio
    if len(df) == 0:
        print(f"❌ Arquivo está vazio: {caminho}")
        return None
    
    print(f"✅ Carregado: {len(df)} linhas")
    return df


# ============================================
# DEMONSTRAÇÃO
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DEMONSTRAÇÃO: TRATAMENTO DE ERROS")
    print("="*60)
    
    # Teste 1: Arquivo que existe
    print("\n--- Teste 1: Arquivo existe ---")
    df = carregar_v3('data/transacoes.csv')
    
    # Teste 2: Arquivo que não existe
    print("\n--- Teste 2: Arquivo não existe ---")
    df = carregar_v3('data/nao_existe.csv')
    
    # Teste 3: Arquivo não é CSV
    print("\n--- Teste 3: Não é CSV ---")
    df = carregar_v3('data/arquivo.txt')
    
    print("\n" + "="*60)
    print("CONCLUSÃO")
    print("="*60)
    print("""
SEM tratamento:
  → Erro confuso do Python
  → Usuário não sabe o que fazer

COM tratamento:
  → Mensagem clara
  → Pipeline pode decidir o que fazer
  → Mais fácil debugar
    """)
