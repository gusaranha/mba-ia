"""
Job de re-treinamento simplificado para demo do DVC.
"""
import pandas as pd
import numpy as np
import pickle
import logging
from pathlib import Path
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Configuração
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

MODELO_PRODUCAO = Path("models/modelo_em_producao.pkl")
MODELO_ARQUIVO = Path("models/arquivo")
DADOS_TESTE = Path("data/teste_fixo.csv")


def carregar_dados() -> pd.DataFrame:
    """Carrega dados de transacoes.csv"""
    dados = pd.read_csv("data/transacoes.csv")
    log.info(f"✓ {len(dados):,} transações carregadas")
    return dados


def preparar_features(dados: pd.DataFrame) -> tuple:
    """Prepara features para treino."""
    X = pd.get_dummies(dados[['valor', 'hora', 'dia_semana', 'categoria']])
    y = dados['is_fraude']
    return X, y


def treinar_modelo(X, y) -> RandomForestClassifier:
    """Treina modelo RandomForest."""
    modelo = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    modelo.fit(X, y)
    log.info("✓ Modelo treinado")
    return modelo


def obter_teste_fixo() -> tuple:
    """Obtém dados de teste fixos."""
    if DADOS_TESTE.exists():
        dados = pd.read_csv(DADOS_TESTE)
    else:
        log.info("Criando conjunto de teste fixo...")
        np.random.seed(12345)
        n = 10000
        valor = np.random.exponential(500, n)
        hora = np.random.randint(0, 24, n)
        dia_semana = np.random.randint(0, 7, n)
        categoria = np.random.choice(['A', 'B', 'C', 'D'], n)
        
        score = np.zeros(n)
        score += (valor > 800) * 0.4
        score += ((hora >= 22) | (hora <= 5)) * 0.3
        score += (categoria == 'D') * 0.2
        score += 0.02
        is_fraude = (np.random.random(n) < score).astype(int)
        
        dados = pd.DataFrame({
            'valor': valor, 'hora': hora, 'dia_semana': dia_semana,
            'categoria': categoria, 'is_fraude': is_fraude
        })
        dados.to_csv(DADOS_TESTE, index=False)
    
    return preparar_features(dados)


def avaliar(modelo, X_teste, y_teste) -> float:
    """Calcula F1-score."""
    y_pred = modelo.predict(X_teste)
    return f1_score(y_teste, y_pred)


def executar_job():
    """Executa o job completo."""
    log.info("=" * 50)
    log.info("JOB DE RE-TREINAMENTO")
    log.info("=" * 50)
    
    # 1. Carregar e treinar
    dados = carregar_dados()
    X, y = preparar_features(dados)
    modelo_novo = treinar_modelo(X, y)
    
    # 2. Avaliar
    X_teste, y_teste = obter_teste_fixo()
    f1_novo = avaliar(modelo_novo, X_teste, y_teste)
    
    # 3. Comparar com atual
    if MODELO_PRODUCAO.exists():
        with open(MODELO_PRODUCAO, 'rb') as f:
            modelo_atual = pickle.load(f)
        f1_atual = avaliar(modelo_atual, X_teste, y_teste)
    else:
        f1_atual = 0.0
        log.info("  (Primeiro modelo)")
    
    log.info(f"  F1 atual: {f1_atual:.4f}")
    log.info(f"  F1 novo:  {f1_novo:.4f}")
    
    # 4. Decidir
    if f1_novo >= f1_atual:
        log.info("✓ Modelo novo é melhor ou igual")
        
        # Arquivar anterior
        if MODELO_PRODUCAO.exists():
            MODELO_ARQUIVO.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo = MODELO_ARQUIVO / f"modelo_{timestamp}.pkl"
            MODELO_PRODUCAO.rename(arquivo)
            log.info(f"  Anterior arquivado: {arquivo.name}")
        
        # Salvar novo
        MODELO_PRODUCAO.parent.mkdir(parents=True, exist_ok=True)
        with open(MODELO_PRODUCAO, 'wb') as f:
            pickle.dump(modelo_novo, f)
        log.info("✓ Modelo em produção atualizado")
    else:
        log.info("✗ Modelo novo é PIOR - mantendo atual")
    
    log.info("=" * 50)
    log.info("FIM DO JOB")
    log.info("=" * 50)


if __name__ == "__main__":
    executar_job()
