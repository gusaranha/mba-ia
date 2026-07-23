# ENCONTRO 1: TOOLS AVANÇADAS + ReAct APROFUNDADO
# Script 1: Tools Refatoradas para 4 Datasets SINARM

"""
OBJETIVO: Criar Tools robustas para consultar 4 datasets SINARM reais
ENCONTRO 1 - ATIVIDADE 1

Datasets:
1. OCORRENCIAS (74.758 linhas) - Furtos, apreensões, recuperações
2. PORTES (2.328 linhas) - Portes de armas (status, validade)
3. REGISTROS (12.798 linhas) - Registros de armas para defesa pessoal
4. REQUERIMENTOS (46.116 linhas) - Requerimentos de porte/registro

O que aluno vai aprender:
- Cache para performance (3 CSVs grandes)
- Validação rigorosa de input
- Logging para auditoria
- Tratamento de erro
- Output estruturado (JSON)
- Conformidade LGPD (sem "idade")
- Multi-dataset investigation
"""

import logging
import json
import pandas as pd
from pathlib import Path
from functools import lru_cache
from datetime import datetime
from typing import List, Dict, Any, Union
from langchain_core.tools import tool

# ========== CONFIGURAÇÃO ==========

import sys
import io
import os

# Corrigir encoding no Windows (Python 3.7+)
os.environ['PYTHONIOENCODING'] = 'utf-8'

if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
elif sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sinarm_queries.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Caminhos
BASE_DIR = Path(__file__).resolve().parents[1]
print(BASE_DIR)
ARQUIVOS_DIR = BASE_DIR / "DADOS_SINARM"

# Datasets com configuração
DATASETS = {
    "ocorrencias": {
        "path": ARQUIVOS_DIR / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
        "sep": ";",
        "encoding": "latin-1",
        "description": "Furtos, apreensões, recuperações de armas",
        "linhas": 74758
    },
    "portes": {
        "path": ARQUIVOS_DIR / "PORTES" / "PORTES_2026.csv",
        "sep": ";",
        "encoding": "latin-1",
        "description": "Portes de armas (status, validade)",
        "linhas": 2328
    },
    "registros": {
        "path": ARQUIVOS_DIR / "REGISTROS" / "REGISTROS_com_categoria_2026.csv",
        "sep": ";",
        "encoding": "latin-1",
        "description": "Registros de armas para defesa pessoal",
        "linhas": 12798
    },
    "requerimentos": {
        "path": ARQUIVOS_DIR / "REQUERIMENTOS" / "REQUERIMENTOS_com_categoria_2026.csv",
        "sep": ";",
        "encoding": "latin-1",
        "description": "Requerimentos de porte/registro",
        "linhas": 46116
    }
}

# ========== CACHE DE DADOS ==========

_df_cache: Dict[str, pd.DataFrame] = {}

@lru_cache(maxsize=4)
def _load_dataset(dataset_name: str) -> pd.DataFrame:
    """Carregar dataset com cache para performance."""
    
    if dataset_name not in DATASETS:
        raise ValueError(f"Dataset '{dataset_name}' não conhecido")
    
    config = DATASETS[dataset_name]
    
    if not config["path"].exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {config['path']}")
    
    try:
        logger.info(f"Carregando {dataset_name} de {config['path']}")
        df = pd.read_csv(
            config["path"],
            sep=config["sep"],
            encoding=config["encoding"]
        )
        logger.info(f"✅ {dataset_name} carregado: {len(df):,} linhas, {len(df.columns)} colunas")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar {dataset_name}: {str(e)}")
        raise

# ========== VALIDAÇÃO ==========

def _validar_query(query: str) -> tuple[str, str]:
    """Validar e parsear query no formato 'campo:valor'."""
    
    # Check 1: Formato
    if not query or ":" not in query:
        raise ValueError("Formato inválido. Use 'campo:valor' (ex: 'marca:Taurus')")
    
    # Check 2: Tamanho
    if len(query) > 1000:
        raise ValueError("Query muito longa (máx 1000 caracteres)")
    
    # Check 3: Injeção SQL
    sql_patterns = ["DROP", "DELETE", "INSERT", "UPDATE", "--", ";"]
    if any(pattern.upper() in query.upper() for pattern in sql_patterns):
        logger.warning(f"SQL injection suspeito: {query}")
        raise ValueError("Query contém padrão suspeito (possível SQL injection)")
    
    # Parse
    campo, valor = query.split(":", 1)
    campo = campo.strip()
    valor = valor.strip()
    
    # Check 4: Valor vazio
    if not valor:
        raise ValueError("Valor não pode estar vazio")
    
    logger.info(f"Query validada: campo={campo}, valor={valor[:50]}")
    return campo, valor

# ========== MAPEAR COLUNAS ==========

def _mapear_coluna(df: pd.DataFrame, campo: str) -> str:
    """Mapear nome de campo para coluna real do DataFrame."""
    
    df_columns = {col.strip().lower(): col for col in df.columns}
    campo_lower = campo.lower()
    
    # Mapeamento inteligente
    mapeamentos = {
        "marca": ["marca_arma"],
        "tipo": ["tipo_ocorrencia", "tipo"],
        "especie": ["especie_arma"],
        "calibre": ["calibre_arma"],
        "municipio": ["municipio"],
        "uf": ["uf"],
        "ano": ["ano_ocorrencia", "ano_emissao", "ano"],
        "mes": ["mes_ocorrencia", "mes_missao", "mes"],
        "status": ["status_porte", "status_registro", "status"],
        "sexo": ["sexo"],
        "categoria": ["categoria"],
        "decisao": ["decisao"],
        "abrangencia": ["abrangencia"],
        "tipo_requerimento": ["tipo_requerimento"]
    }
    
    # Procurar mapeamento
    if campo_lower in mapeamentos:
        for alias in mapeamentos[campo_lower]:
            if alias in df_columns:
                return df_columns[alias]
    
    # Busca direta (case-insensitive)
    if campo_lower in df_columns:
        return df_columns[campo_lower]
    
    # Nada encontrado
    colunas_disponiveis = list(df.columns)[:10]
    raise ValueError(
        f"Campo '{campo}' não encontrado.\n"
        f"Colunas disponíveis: {', '.join(colunas_disponiveis)}"
    )

# ========== BUSCA GENÉRICA ==========

def _buscar_impl(query: str, dataset: str) -> Union[List[Dict], Dict]:
    """Implementação genérica da busca."""
    
    try:
        # 1. Validar
        campo, valor = _validar_query(query)
        
        # 2. Carregar
        df = _load_dataset(dataset)
        
        # 3. Mapear coluna
        col = _mapear_coluna(df, campo)
        
        # 4. Buscar
        mask = df[col].astype(str).str.contains(valor, case=False, na=False)
        resultados = df[mask].copy()
        
        # 5. Remover "idade" (Nota Técnica PF 15/02/2024)
        colunas_drop = [c for c in resultados.columns if c.lower() == 'idade']
        if colunas_drop:
            resultados = resultados.drop(columns=colunas_drop)
            logger.info("✅ Campo 'idade' removido (conformidade)")
        
        # 6. Converter para dict
        records = resultados.to_dict(orient='records')
        
        # 7. Adicionar auditoria
        for r in records:
            r['fonte_arquivo'] = f"{DATASETS[dataset]['description']}"
            r['timestamp_consulta'] = datetime.now().isoformat()
        
        # 8. Log
        logger.info(f"Busca OK: {len(records)} registros em {dataset}")
        
        if len(records) == 0:
            return [{
                "fonte_arquivo": f"{DATASETS[dataset]['description']}",
                "mensagem": f"Nenhuma ocorrência encontrada para {campo}={valor}",
                "campo_consultado": campo,
                "valor_consultado": valor,
                "dataset": dataset
            }]
        
        return records
        
    except Exception as e:
        logger.error(f"Erro na busca: {str(e)}")
        return {
            "erro": str(e),
            "dataset": dataset,
            "tipo_erro": type(e).__name__
        }

# ========== TOOLS (Decorados para LangChain) ==========

@tool
def buscar_ocorrencias(query: str) -> str:
    """
    Busca ocorrências de armas (furtos, apreensões, recuperações).
    
    DATASET: OCORRENCIAS_2026.csv (74.758 registros)
    
    Args:
        query: Formato "campo:valor"
               Exemplos: "marca:Taurus", "tipo:Furto", "uf:DF", "especie:Pistola"
    
    Colunas disponíveis:
        - marca (ex: Taurus, Rossi, Beretta)
        - tipo (ex: Furto, Apreensão, Recuperação)
        - especie (ex: Pistola, Revólver)
        - calibre (ex: .380, 9mm)
        - uf (ex: DF, SP, RJ)
        - municipio
        - ano, mes
    
    Returns:
        JSON com registros + auditoria
    
    Conformidade:
        - Remove campo "idade" (Nota Técnica PF 15/02/2024)
        - Inclui fonte para auditoria
        - Loga para rastreamento
    """
    resultado = _buscar_impl(query, dataset="ocorrencias")
    return json.dumps(resultado, ensure_ascii=False)

@tool
def buscar_portes(query: str) -> str:
    """
    Busca portes de armas de fogo (defesa pessoal).
    
    DATASET: PORTES_2026.csv (2.328 registros)
    
    Args:
        query: Formato "campo:valor"
               Exemplos: "status:Válido", "uf:DF", "marca:Taurus"
    
    Colunas disponíveis:
        - status (ex: Válido, Vencido)
        - uf, municipio
        - marca, especie, calibre
        - tipo (ex: Defesa)
        - ano, mes
    
    Returns:
        JSON com registros + auditoria
    """
    resultado = _buscar_impl(query, dataset="portes")
    return json.dumps(resultado, ensure_ascii=False)

@tool
def buscar_registros(query: str) -> str:
    """
    Busca registros de armas de fogo (defesa pessoal).
    
    DATASET: REGISTROS_com_categoria_2026.csv (12.798 registros)
    
    Args:
        query: Formato "campo:valor"
               Exemplos: "marca:Taurus", "status:Ativo", "categoria:CAC"
    
    Colunas disponíveis:
        - marca, especie, calibre
        - status_registro (ex: Ativo, Cancelado)
        - categoria (ex: CAC, Defesa)
        - uf, municipio
        - ano, mes
    
    Returns:
        JSON com registros + auditoria
    """
    resultado = _buscar_impl(query, dataset="registros")
    return json.dumps(resultado, ensure_ascii=False)

@tool
def buscar_requerimentos(query: str) -> str:
    """
    Busca requerimentos de porte/registro.
    
    DATASET: REQUERIMENTOS_com_categoria_2026.csv (46.116 registros)
    
    Args:
        query: Formato "campo:valor"
               Exemplos: "decisao:Aprovado", "tipo_requerimento:Porte", "uf:DF"
    
    Colunas disponíveis:
        - tipo_requerimento
        - decisao (ex: Aprovado, Negado, Aguardando)
        - categoria (ex: CAC, Defesa)
        - uf, municipio
        - ano, mes
    
    Returns:
        JSON com registros + auditoria
    """
    resultado = _buscar_impl(query, dataset="requerimentos")
    return json.dumps(resultado, ensure_ascii=False)

# ========== FUNÇÕES HELPER ==========

def listar_colunas(dataset: str) -> List[str]:
    """Listar colunas disponíveis."""
    try:
        df = _load_dataset(dataset)
        return list(df.columns)
    except Exception as e:
        logger.error(f"Erro: {e}")
        return []

def amostra_dados(dataset: str, n: int = 3) -> Dict:
    """Retornar amostra de dados."""
    try:
        df = _load_dataset(dataset)
        amostra = df.head(n).to_dict(orient='records')
        return {
            "dataset": dataset,
            "descricao": DATASETS[dataset]["description"],
            "total_linhas": len(df),
            "total_colunas": len(df.columns),
            "colunas": list(df.columns),
            "amostra": amostra
        }
    except Exception as e:
        logger.error(f"Erro: {e}")
        return {"erro": str(e)}

def estatisticas(dataset: str) -> Dict:
    """Retornar estatísticas do dataset."""
    try:
        df = _load_dataset(dataset)
        return {
            "dataset": dataset,
            "descricao": DATASETS[dataset]["description"],
            "total_linhas": len(df),
            "total_colunas": len(df.columns),
            "colunas": list(df.columns),
            "tamanho_mb": DATASETS[dataset]["path"].stat().st_size / 1024 / 1024
        }
    except Exception as e:
        return {"erro": str(e)}

# ========== TESTES ==========

if __name__ == "__main__":
    print("\n=== TESTE TOOLS SINARM ===\n")
    
    # Test 1: Ocorrências
    print("TEST 1: Busca Ocorrências")
    resultado = _buscar_impl("marca:Taurus", "ocorrencias")
    print(f"✅ {len(resultado)} registros\n")
    
    # Test 2: Portes
    print("TEST 2: Busca Portes")
    resultado = _buscar_impl("status:Válido", "portes")
    print(f"✅ {len(resultado)} registros\n")
    
    # Test 3: Registros
    print("TEST 3: Busca Registros")
    resultado = _buscar_impl("marca:Taurus", "registros")
    print(f"✅ {len(resultado)} registros\n")
    
    # Test 4: Requerimentos
    print("TEST 4: Busca Requerimentos")
    resultado = _buscar_impl("decisao:Aprovado", "requerimentos")
    print(f"✅ {len(resultado)} registros\n")
    
    # Test 5: SQL Injection
    print("TEST 5: Proteção SQL Injection")
    try:
        _buscar_impl("marca:Taurus'; DROP TABLE--", "ocorrencias")
    except ValueError as e:
        print(f"✅ Rejeitado: {e}\n")
    
    print("=== FIM DOS TESTES ===")
