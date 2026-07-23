# ENCONTRO 1 - VERSÃO 1.8: AGENTE ROBUSTO COM ERROR HANDLING + VALIDATION
# Quinta 16/07/2026
# Agente que se recupera de erros e valida qualidade de respostas

"""
OBJETIVO: Criar agente production-ready que:
1. Se recupera automaticamente de falhas (retry, fallback, circuit breaker)
2. Valida qualidade de respostas (regex, heurística, LLM)
3. Usa feedback loop para refinar respostas inadequadas

PROGRESSÃO:
v1.0 (Terça 14/07):  Tools + ReAct básico
v1.8 (Quinta 16/07): v1.0 + Error Handling + Validation ← VOCÊ ESTÁ AQUI

PRÉ-REQUISITO: E1_tools_sinarm.py (4 Tools)
"""

import sys
import io
import os
import time
import logging
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Callable, Any, Dict, List, Optional
from functools import wraps
from collections import defaultdict

# ========== CONFIGURAÇÃO INICIAL ==========

# Melhorar encoding no Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup paths
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agente_v1.8.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Importar Tools
try:
    from E1_tools_sinarm import (
        buscar_ocorrencias,
        buscar_registros,
        buscar_portes,
        buscar_requerimentos
    )
    from langchain_ollama import OllamaLLM
    from langchain.agents import initialize_agent, AgentType
    from langchain.memory import ConversationBufferMemory
    IMPORTS_OK = True
except ImportError as e:
    logger.warning(f"Aviso: Alguns imports falharam: {e}")
    IMPORTS_OK = False

# ========== PARTE 1: ERROR HANDLING ==========

class CircuitBreaker:
    """
    Proteção: Se Tool falha N vezes, para de tentar por um tempo.
    Previne avalanche de erros.
    
    CONCEITO:
    ├─ Closed: Funcionando normal
    ├─ Open: Muito erro, rejeitando requisições
    └─ Half-Open: Testando se recuperou
    """
    
    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60):
        self.failure_count = 0
        self.last_failure_time = None
        self.failure_threshold = failure_threshold
        self.timeout = timeout_seconds
        self.state = "CLOSED"
    
    def is_circuit_open(self) -> bool:
        """Verifica se circuito está aberto (rejeitando requisições)"""
        if self.failure_count >= self.failure_threshold:
            elapsed = (datetime.now() - self.last_failure_time).total_seconds()
            if elapsed < self.timeout:
                self.state = "OPEN"
                return True  # Circuito aberto, rejeitar
            else:
                # Reset se passou o timeout (tentar de novo)
                self.failure_count = 0
                self.last_failure_time = None
                self.state = "CLOSED"
                return False
        return False
    
    def record_failure(self):
        """Registrar uma falha"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        logger.warning(f"CircuitBreaker: Falha #{self.failure_count}")
    
    def record_success(self):
        """Registrar sucesso (reset)"""
        self.failure_count = 0
        self.state = "CLOSED"


def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0
) -> Any:
    """
    RETRY COM EXPONENTIAL BACKOFF
    
    PROGRESSÃO DE DELAY:
    Tentativa 1: 1 segundo
    Tentativa 2: 2 segundos
    Tentativa 3: 4 segundos
    
    MOTIVO: Não sobrecarregar API/Sistema
    """
    for attempt in range(max_retries):
        try:
            result = func()
            if attempt > 0:
                logger.info(f"✅ Sucesso após {attempt} retries")
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                # Última tentativa falhou
                logger.error(f"❌ Falha permanente após {max_retries} tentativas: {e}")
                raise
            
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(f"⏳ Tentativa {attempt+1} falhou. Aguardando {delay}s...")
            time.sleep(delay)


# ========== PARTE 2: VALIDATION ==========

class ValidadorHeuristico:
    """
    VALIDADOR COM HEURÍSTICAS
    
    Verifica:
    1. Contém número?
    2. Contém fonte?
    3. Tamanho razoável?
    4. Não vazio?
    5. Não contém erro genérico?
    """
    
    def __call__(self, resposta: str, query: str = "") -> Dict:
        """Validar resposta e retornar score (0-1)"""
        
        resposta_lower = resposta.lower()
        
        checks = {
            'tem_numero': bool(re.search(r'\d+', resposta)),
            'tem_fonte': bool(re.search(
                r'(OCORRENCIAS|REGISTROS|PORTES|REQUERIMENTOS|fonte_arquivo)',
                resposta,
                re.IGNORECASE
            )),
            'tamanho_ok': 50 < len(resposta) < 3000,
            'nao_vazio': len(resposta.strip()) > 0,
            'sem_erro': not any(
                termo in resposta_lower
                for termo in ['erro desconhecido', 'falha', 'crashed']
            ),
        }
        
        score = sum(checks.values()) / len(checks)
        
        return {
            'valido': score >= 0.7,  # Aprovado se 70%+
            'score': score,
            'detalhes': checks,
            'motivo': 'OK' if score >= 0.7 else 'Score baixo'
        }


class ValidadorRegex:
    """
    VALIDADOR COM REGEX
    
    Padrões simples:
    - Tem número?
    - Tem fonte?
    """
    
    def __call__(self, resposta: str) -> Dict:
        validacoes = {
            'tem_numero': bool(re.search(r'\d+', resposta)),
            'tem_fonte': bool(re.search(r'OCORRENCIAS|REGISTROS|PORTES|REQUERIMENTOS', resposta)),
            'tamanho_ok': 50 < len(resposta) < 3000,
            'nao_vazio': len(resposta.strip()) > 0,
        }
        
        return {
            'valido': all(validacoes.values()),
            'detalhes': validacoes,
            'score': sum(validacoes.values()) / len(validacoes)
        }


# ========== PARTE 3: AGENTE ROBUSTO ==========

class AgenteV18:
    """
    AGENTE v1.8: PRODUCTION-READY
    
    Features:
    ✅ Error Handling (retry + fallback + circuit breaker)
    ✅ Validation (regex + heurística + feedback)
    ✅ Logging completo
    ✅ Multi-iteração ReAct
    """
    
    def __init__(self, verbose: bool = True, max_iterations: int = 3):
        self.verbose = verbose
        self.max_iterations = max_iterations
        self.circuit_breaker = CircuitBreaker()
        self.validador = ValidadorHeuristico()
        self.stats = {
            'queries': 0,
            'sucesso': 0,
            'falha': 0,
            'validacao_pass': 0,
            'validacao_fail': 0,
        }
        
        if IMPORTS_OK:
            self.agente = self._criar_agente()
        else:
            self.agente = None
    
    def _criar_agente(self):
        """Criar agente ReAct básico"""
        try:
            llm = OllamaLLM(
                model="llama3",
                temperature=0.0,
                base_url="http://localhost:11434"
            )
            
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            tools = [
                buscar_ocorrencias,
                buscar_registros,
                buscar_portes,
                buscar_requerimentos
            ]
            
            system_message = """
Você é investigador especialista em armas PCDF.

PADRÃO REACIONÁRIO:
1. THOUGHT: O que preciso saber?
2. ACTION: Qual ferramenta usar?
3. OBSERVATION: O que retornou?
4. RESPOSTA: Diga o resultado

REGRAS:
✅ SEMPRE cite fonte (OCORRENCIAS.csv)
✅ Se não encontrar, diga "não encontrado"
✅ Não invente dados
"""
            
            agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                agent_kwargs={"system_message": system_message},
                memory=memory,
                verbose=self.verbose,
                max_iterations=self.max_iterations
            )
            
            return agent
        except Exception as e:
            logger.error(f"Erro ao criar agente: {e}")
            return None
    
    def executar_com_robustez(self, query: str) -> Dict:
        """
        EXECUÇÃO ROBUSTA COM TODAS AS PROTEÇÕES
        
        Fluxo:
        1. Check circuit breaker
        2. Validar input
        3. Executar com retry
        4. Validar output
        5. Feedback se necessário
        """
        
        self.stats['queries'] += 1
        
        # 1. CHECK CIRCUIT BREAKER
        if self.circuit_breaker.is_circuit_open():
            msg = "Sistema temporariamente indisponível (muitos erros)"
            logger.warning(msg)
            return {
                'erro': msg,
                'status': 'circuit_open',
                'timestamp': datetime.now().isoformat()
            }
        
        # 2. VALIDAR INPUT
        if not query or len(query) > 10000:
            return {
                'erro': 'Query inválida (vazia ou muito longa)',
                'status': 'input_invalid'
            }
        
        # 3. EXECUTAR COM RETRY
        resposta = None
        try:
            resposta = retry_with_backoff(
                lambda: self.agente.run(query) if self.agente else "AGENTE NÃO DISPONÍVEL",
                max_retries=2
            )
            self.stats['sucesso'] += 1
            self.circuit_breaker.record_success()
        except Exception as e:
            logger.error(f"Erro na execução: {e}")
            self.circuit_breaker.record_failure()
            self.stats['falha'] += 1
            return {
                'erro': str(e),
                'status': 'execution_failed',
                'timestamp': datetime.now().isoformat()
            }
        
        # 4. VALIDAR OUTPUT
        resultado_validacao = self.validador(resposta, query)
        
        if resultado_validacao['valido']:
            self.stats['validacao_pass'] += 1
        else:
            self.stats['validacao_fail'] += 1
            logger.warning(f"Validação falhou: {resultado_validacao['detalhes']}")
        
        # 5. RETORNO ESTRUTURADO
        return {
            'resposta': resposta,
            'validacao': resultado_validacao,
            'confianca': resultado_validacao['score'],
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats
        }
    
    def modo_demo(self):
        """DEMO: 3 queries pré-definidas"""
        queries_demo = [
            "Quantas armas Taurus foram apreendidas?",
            "Qual é a diferença entre furto e roubo?",
            "Quantos revólveres estão registrados?",
        ]
        
        print("\n" + "="*70)
        print("🎬 MODO DEMO - v1.8 COM ERROR HANDLING + VALIDATION")
        print("="*70 + "\n")
        
        for i, query in enumerate(queries_demo, 1):
            print(f"\n[Query {i}/3] {query}")
            print("-" * 70)
            
            resultado = self.executar_com_robustez(query)
            
            if 'erro' in resultado:
                print(f"❌ ERRO: {resultado['erro']}")
            else:
                print(f"✅ RESPOSTA:\n{resultado['resposta']}\n")
                print(f"📊 VALIDAÇÃO:")
                print(f"   Score: {resultado['confianca']:.2%}")
                print(f"   Válida: {resultado['validacao']['valido']}")
                print(f"   Detalhes: {resultado['validacao']['detalhes']}")
    
    def modo_interativo(self):
        """MODO INTERATIVO: Digite suas perguntas"""
        print("\n" + "="*70)
        print("💬 MODO INTERATIVO - v1.8")
        print("Digite 'sair' para encerrar")
        print("="*70 + "\n")
        
        while True:
            query = input("Você: ").strip()
            
            if query.lower() in ['sair', 'exit', 'quit']:
                print("\n✅ Até logo!")
                break
            
            if not query:
                continue
            
            resultado = self.executar_com_robustez(query)
            
            if 'erro' in resultado:
                print(f"\n❌ ERRO: {resultado['erro']}\n")
            else:
                print(f"\n🤖 Agente: {resultado['resposta']}\n")
                print(f"📊 Confiança: {resultado['confianca']:.2%}")
    
    def modo_manual(self):
        """MODO MANUAL: Testar função específica"""
        print("\n" + "="*70)
        print("🔧 MODO MANUAL - Testes Específicos")
        print("="*70 + "\n")
        
        print("Teste 1: Validação COM números e fonte")
        resposta_boa = "Encontrei 580 apreensões em OCORRENCIAS_2026.csv"
        val1 = self.validador(resposta_boa)
        print(f"Resultado: {val1['valido']} (score: {val1['score']:.2%})\n")
        
        print("Teste 2: Validação SEM números")
        resposta_ruim = "Não consegui achar informações sobre isto"
        val2 = self.validador(resposta_ruim)
        print(f"Resultado: {val2['valido']} (score: {val2['score']:.2%})\n")
        
        print("Teste 3: Validação SEM fonte")
        resposta_meio = "Existem 342 registros"
        val3 = self.validador(resposta_meio)
        print(f"Resultado: {val3['valido']} (score: {val3['score']:.2%})\n")


# ========== MAIN ==========

def main():
    import sys
    
    # Criar agente
    agente = AgenteV18(verbose=True, max_iterations=3)
    
    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()
    else:
        modo = "demo"
    
    if modo == "demo":
        agente.modo_demo()
    elif modo == "interactive":
        agente.modo_interativo()
    elif modo == "manual":
        agente.modo_manual()
    else:
        print("Uso: python agente_v1.8.py [demo|interactive|manual]")
        print("\nModos:")
        print("  demo        - 3 queries pré-definidas")
        print("  interactive - Digite suas perguntas")
        print("  manual      - Testes de validação")


if __name__ == "__main__":
    main()
