"""
Demonstração: Organizar código em funções
Compara código misturado vs código organizado em funções
"""

import pandas as pd
import numpy as np


# ============================================
# VERSÃO 1: Código misturado (como Maria tinha)
# ============================================

def processar_v1():
    """Versão original - tudo junto"""
    print("\n" + "="*50)
    print("VERSÃO 1: Código Misturado")
    print("="*50)
    
    df = pd.read_csv('data/transacoes.csv')
    df = df.dropna()
    df = df.drop_duplicates()
    df['valor_log'] = np.log1p(df['valor'])
    df.to_csv('data/processado_v1.csv', index=False)
    print(f"✅ Processado: {len(df)} linhas")


# ============================================
# VERSÃO 2: Código em funções
# ============================================

def extrair_dados(caminho):
    """Lê dados de arquivo CSV"""
    df = pd.read_csv(caminho)
    print(f"  Extraído: {len(df)} linhas")
    return df


def limpar_dados(df):
    """Remove nulos e duplicatas"""
    antes = len(df)
    df = df.dropna()
    df = df.drop_duplicates()
    depois = len(df)
    print(f"  Limpeza: {antes} → {depois} linhas")
    return df


def criar_features(df):
    """Cria features derivadas"""
    df = df.copy()
    df['valor_log'] = np.log1p(df['valor'])
    print(f"  Features criadas: valor_log")
    return df


def salvar_dados(df, caminho):
    """Salva dados processados"""
    df.to_csv(caminho, index=False)
    print(f"  Salvo em: {caminho}")


def processar_v2():
    """Versão organizada - funções separadas"""
    print("\n" + "="*50)
    print("VERSÃO 2: Funções Separadas")
    print("="*50)
    
    print("\n1. Extraindo...")
    df = extrair_dados('data/transacoes.csv')
    
    print("\n2. Limpando...")
    df = limpar_dados(df)
    
    print("\n3. Criando features...")
    df = criar_features(df)
    
    print("\n4. Salvando...")
    salvar_dados(df, 'data/processado_v2.csv')
    
    print("\n✅ Pipeline concluído!")


# ============================================
# COMPARAÇÃO
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DEMONSTRAÇÃO: CÓDIGO MISTURADO vs FUNÇÕES")
    print("="*60)
    
    processar_v1()
    processar_v2()
    
    print("\n" + "="*60)
    print("COMPARAÇÃO")
    print("="*60)
    print("""
VERSÃO 1 (misturado):
  ❌ Difícil saber onde está cada etapa
  ❌ Impossível testar partes isoladas
  ❌ Difícil reusar código

VERSÃO 2 (funções):
  ✅ Cada etapa é clara
  ✅ Pode testar cada função separadamente
  ✅ Pode reusar funções em outros projetos
  ✅ Sabe exatamente onde quebrou se der erro
    """)
