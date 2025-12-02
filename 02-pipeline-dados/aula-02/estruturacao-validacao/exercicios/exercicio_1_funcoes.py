"""
Exercício 1: Organizar código em funções

Código misturado abaixo. Sua tarefa:
- Criar funções separadas
- Organizar em pipeline
"""

import pandas as pd
import numpy as np


# ============================================
# CÓDIGO MISTURADO (não modificar)
# ============================================

def processar_original():
    """Código original - tudo junto"""
    df = pd.read_csv('data/vendas.csv')
    df = df.dropna()
    df = df.drop_duplicates()
    df['preco_log'] = np.log1p(df['preco'])
    df.to_csv('data/vendas_processado.csv', index=False)
    print("Feito!")


# ============================================
# TODO: CRIAR FUNÇÕES SEPARADAS
# ============================================

# TODO 1: Criar função extrair_dados(caminho)
# Deve: ler CSV e retornar DataFrame



# TODO 2: Criar função limpar_dados(df)
# Deve: remover nulos e duplicatas, retornar DataFrame



# TODO 3: Criar função criar_features(df)
# Deve: criar coluna preco_log, retornar DataFrame



# TODO 4: Criar função salvar_dados(df, caminho)
# Deve: salvar DataFrame em CSV



# TODO 5: Criar função executar_pipeline()
# Deve: chamar as funções acima na ordem correta



# ============================================
# TESTE
# ============================================

if __name__ == "__main__":
    # Descomentar quando implementar:
    # executar_pipeline()
    pass
