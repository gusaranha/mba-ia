"""
Demo 9: Versão "produção" do código
Objetivo: Mostrar estrutura adequada para produção
"""

import os
import logging
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from datetime import datetime

# ============================================
# CONFIGURAÇÃO
# ============================================

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Caminhos relativos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')

# Criar diretório de modelos se não existir
os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================
# FUNÇÕES
# ============================================

def carregar_dados(arquivo):
    """
    Carrega dados com tratamento de erro
    
    Args:
        arquivo: nome do arquivo CSV
    
    Returns:
        DataFrame com dados carregados
    
    Raises:
        FileNotFoundError: se arquivo não existe
        Exception: outros erros de leitura
    """
    try:
        caminho = os.path.join(DATA_DIR, arquivo)
        logger.info(f"Carregando dados de {caminho}")
        
        df = pd.read_csv(caminho)
        logger.info(f"✅ {len(df):,} transações carregadas")
        
        return df
        
    except FileNotFoundError:
        logger.error(f"❌ Arquivo não encontrado: {arquivo}")
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao carregar dados: {e}")
        raise


def preparar_features(df):
    """
    Prepara features com validação
    
    Args:
        df: DataFrame com dados brutos
    
    Returns:
        tuple: (X, y, label_encoder)
    
    Raises:
        ValueError: se colunas necessárias estão ausentes
    """
    try:
        logger.info("Preparando features...")
        
        # Validar colunas necessárias
        colunas_necessarias = ['valor', 'hora', 'categoria', 'is_fraud']
        colunas_faltantes = set(colunas_necessarias) - set(df.columns)
        
        if colunas_faltantes:
            raise ValueError(f"Colunas faltantes: {colunas_faltantes}")
        
        # Converter categoria
        le = LabelEncoder()
        df['categoria_cod'] = le.fit_transform(df['categoria'])
        
        X = df[['valor', 'hora', 'categoria_cod']]
        y = df['is_fraud']
        
        logger.info(f"✅ Features preparadas: {X.shape}")
        return X, y, le
        
    except Exception as e:
        logger.error(f"❌ Erro ao preparar features: {e}")
        raise


def treinar_modelo(X_train, y_train):
    """
    Treina modelo com configuração fixa
    
    Args:
        X_train: features de treino
        y_train: target de treino
    
    Returns:
        modelo treinado
    """
    try:
        logger.info("Treinando modelo...")
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        logger.info("✅ Modelo treinado")
        
        return model
        
    except Exception as e:
        logger.error(f"❌ Erro ao treinar modelo: {e}")
        raise


def avaliar_modelo(model, X_test, y_test):
    """
    Avalia modelo e retorna métricas
    
    Args:
        model: modelo treinado
        X_test: features de teste
        y_test: target de teste
    
    Returns:
        float: F1-Score
    """
    try:
        logger.info("Avaliando modelo...")
        
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred)
        
        logger.info(f"✅ F1-Score: {f1:.4f}")
        return f1
        
    except Exception as e:
        logger.error(f"❌ Erro ao avaliar modelo: {e}")
        raise


def salvar_modelo(model, label_encoder, metricas):
    """
    Salva modelo e metadados
    
    Args:
        model: modelo treinado
        label_encoder: encoder de categorias
        metricas: dict com métricas de avaliação
    """
    try:
        logger.info("Salvando modelo...")
        
        # Salvar modelo
        modelo_path = os.path.join(MODEL_DIR, 'modelo_fraude.pkl')
        with open(modelo_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Salvar encoder
        encoder_path = os.path.join(MODEL_DIR, 'label_encoder.pkl')
        with open(encoder_path, 'wb') as f:
            pickle.dump(label_encoder, f)
        
        # Salvar métricas
        metricas_path = os.path.join(MODEL_DIR, 'metricas.txt')
        with open(metricas_path, 'w') as f:
            f.write(f"F1-Score: {metricas['f1']:.4f}\n")
            f.write(f"Data: {metricas['data']}\n")
        
        logger.info(f"✅ Modelo salvo em {MODEL_DIR}")
        
    except Exception as e:
        logger.error(f"❌ Erro ao salvar modelo: {e}")
        raise


# ============================================
# PIPELINE PRINCIPAL
# ============================================

def main():
    """Pipeline principal de treinamento"""
    try:
        logger.info("=" * 50)
        logger.info("INICIANDO PIPELINE DE TREINAMENTO")
        logger.info("=" * 50)
        
        # 1. Carregar dados
        df = carregar_dados('transacoes_limpas.csv')
        
        # 2. Preparar features
        X, y, le = preparar_features(df)
        
        # 3. Dividir dados
        logger.info("Dividindo dados (70/30)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.3,
            random_state=42,
            stratify=y
        )
        logger.info(f"✅ Treino: {len(X_train):,}, Teste: {len(X_test):,}")
        
        # 4. Treinar modelo
        model = treinar_modelo(X_train, y_train)
        
        # 5. Avaliar modelo
        f1 = avaliar_modelo(model, X_test, y_test)
        
        # 6. Salvar modelo
        metricas = {
            'f1': f1,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        salvar_modelo(model, le, metricas)
        
        logger.info("=" * 50)
        logger.info("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 50)
        
        return model, f1
        
    except Exception as e:
        logger.error("=" * 50)
        logger.error("❌ PIPELINE FALHOU")
        logger.error(f"Erro: {e}")
        logger.error("=" * 50)
        raise


if __name__ == "__main__":
    model, f1 = main()
