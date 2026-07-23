# ENCONTRO 1: AGENTE SIMPLES COM LANGCHAIN 1.3.13+
# Version 3: Agente simplificado que funciona com Ollama

"""
OBJETIVO: Criar agente investigador funcional com Ollama
ENCONTRO 1 - ATIVIDADE 2

Abordagem: Em vez de usar create_agent() (que requer ChatModel com bind_tools),
usamos uma abordagem manual de ReAct mais simples e didática.

O que aluno vai aprender:
- Ciclo ReAct manual (Thought → Action → Observation)
- Como estruturar chamadas a ferramentas
- Debug e logging em produção
"""

import sys
import io
import logging
import os
import json
from pathlib import Path
from typing import Any

# Corrigir encoding Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'

if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup paths
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from langchain_ollama import OllamaLLM

try:
    from E1_tools_sinarm import (
        buscar_ocorrencias,
        buscar_registros,
        buscar_portes,
        buscar_requerimentos
    )
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== MAPEAR FERRAMENTAS ==========

TOOLS_MAP = {
    "buscar_ocorrencias": buscar_ocorrencias if TOOLS_AVAILABLE else None,
    "buscar_registros": buscar_registros if TOOLS_AVAILABLE else None,
    "buscar_portes": buscar_portes if TOOLS_AVAILABLE else None,
    "buscar_requerimentos": buscar_requerimentos if TOOLS_AVAILABLE else None,
}

TOOLS_DESCRIPTIONS = {
    "buscar_ocorrencias": "Busca ocorrências de armas (furtos, apreensões, recuperações). Uso: buscar_ocorrencias(marca=None, status=None)",
    "buscar_registros": "Busca registros de armas defesa pessoal. Uso: buscar_registros(marca=None, status=None)",
    "buscar_portes": "Busca portes de armas. Uso: buscar_portes(marca=None, status=None)",
    "buscar_requerimentos": "Busca requerimentos de porte. Uso: buscar_requerimentos(status=None, decisao=None)",
}

# ========== AGENTE ReAct MANUAL ==========

class AgenteInvestigador:
    """Agente ReAct manual para investigação de armas."""
    
    def __init__(self, verbose: bool = True, max_iterations: int = 3):
        self.llm = OllamaLLM(
            model="llama3",
            temperature=0.0,
            base_url="http://localhost:11434"
        )
        self.verbose = verbose
        self.max_iterations = max_iterations
        self.historico = []
        
        logger.info("✅ Agente inicializado")
    
    def _construir_prompt_system(self) -> str:
        """Constrói prompt de sistema."""
        
        ferramentas_texto = "\n".join([
            f"- {nome}: {desc}"
            for nome, desc in TOOLS_DESCRIPTIONS.items()
        ])
        
        return f"""Você é um ESPECIALISTA EM INVESTIGAÇÃO DE ARMAS da PCDF.

PADRÃO DE RACIOCÍNIO (ReAct):
1. THOUGHT: Analise a pergunta. Qual ferramenta usar?
2. ACTION: Chame a ferramenta apropriada
3. OBSERVATION: Analise o resultado
4. RESPOSTA FINAL: Responda com base nos dados

FERRAMENTAS DISPONÍVEIS:
{ferramentas_texto}

REGRAS:
❌ Não invente dados
❌ Não especule sem dados
✅ SEMPRE cite a fonte
✅ Se não encontrar, diga honestamente

Responda em português do Brasil."""
    
    def _executar_ferramenta(self, nome_ferramenta: str, **kwargs) -> str:
        """Executa uma ferramenta específica."""
        
        if nome_ferramenta not in TOOLS_MAP or not TOOLS_AVAILABLE:
            return f"Ferramenta '{nome_ferramenta}' não disponível"
        
        try:
            tool = TOOLS_MAP[nome_ferramenta]
            resultado = tool(**kwargs)
            
            if self.verbose:
                logger.info(f"  [OBSERVATION] {nome_ferramenta}({kwargs})")
                logger.info(f"  [RESULTADO] {len(str(resultado))} caracteres")
            
            return str(resultado)
        except Exception as e:
            logger.error(f"Erro executando {nome_ferramenta}: {e}")
            return f"Erro: {e}"
    
    def _processar_resposta_llm(self, resposta: str) -> tuple[str, dict]:
        """
        Processa resposta do LLM para detectar ACTION.
        
        Formato esperado:
        THOUGHT: ...
        ACTION: ferramenta_nome(param1=valor1, param2=valor2)
        OBSERVATION: ...
        """
        
        # Tentar extrair ACTION
        if "ACTION:" in resposta:
            try:
                # Extrair linha ACTION
                linhas = resposta.split("\n")
                action_line = None
                for linha in linhas:
                    if "ACTION:" in linha:
                        action_line = linha.replace("ACTION:", "").strip()
                        break
                
                if action_line and "(" in action_line and ")" in action_line:
                    # Parse: ferramenta_nome(param1=valor1, ...)
                    nome_tool = action_line.split("(")[0].strip()
                    
                    # Extrair argumentos
                    args_str = action_line[action_line.index("(")+1:action_line.rindex(")")]
                    
                    # Parse simples de argumentos
                    kwargs = {}
                    if args_str:
                        for par in args_str.split(","):
                            if "=" in par:
                                chave, valor = par.split("=", 1)
                                kwargs[chave.strip()] = valor.strip().strip("'\"")
                    
                    return "action", {"tool": nome_tool, "kwargs": kwargs}
            except Exception as e:
                logger.debug(f"Erro parsing ACTION: {e}")
        
        # Se não há ACTION, é resposta final
        return "response", {}
    
    def invocar(self, pergunta: str) -> str:
        """Executa ciclo ReAct completo."""
        
        print(f"\n🔍 PERGUNTA: {pergunta}\n")
        
        # Prompt inicial
        prompt = f"""{self._construir_prompt_system()}

[HISTÓRICO]
{self._formatar_historico()}

[NOVA PERGUNTA]
{pergunta}

[RESPONDA COM THOUGHT → ACTION → OBSERVATION CONFORME NECESSÁRIO]
"""
        
        # Ciclo ReAct
        for iteracao in range(1, self.max_iterations + 1):
            if self.verbose:
                print(f"--- ITERAÇÃO {iteracao} ---")
            
            # Chamar LLM
            resposta = self.llm.invoke(prompt)
            
            if self.verbose:
                print(f"💭 RESPOSTA LLM:\n{resposta}\n")
            
            # Processar resposta
            tipo, params = self._processar_resposta_llm(resposta)
            
            if tipo == "response":
                # Resposta final
                self.historico.append(("usuario", pergunta))
                self.historico.append(("agente", resposta))
                return resposta
            
            elif tipo == "action":
                # Executar ferramenta
                tool_name = params["tool"]
                kwargs = params["kwargs"]
                
                if self.verbose:
                    print(f"🔧 ACTION: {tool_name}({kwargs})\n")
                
                observation = self._executar_ferramenta(tool_name, **kwargs)
                
                # Adicionar ao prompt para próxima iteração
                prompt += f"\n\n[RESULTADO]:\n{observation}"
        
        # Limite de iterações atingido
        return "⚠️ Limite de iterações atingido. Tente uma pergunta mais simples."
    
    def _formatar_historico(self) -> str:
        """Formata histórico para contexto."""
        if not self.historico:
            return "[Nenhum histórico]"
        
        texto = ""
        for papel, mensagem in self.historico[-4:]:  # Últimas 2 trocas
            prefixo = "👤 USUÁRIO" if papel == "usuario" else "🤖 AGENTE"
            texto += f"\n{prefixo}:\n{mensagem[:200]}...\n"
        return texto


# ========== FUNÇÕES DE INTERFACE ==========

def criar_agente(verbose: bool = True) -> AgenteInvestigador:
    """Cria agente investigador."""
    return AgenteInvestigador(verbose=verbose)


def investigar(pergunta: str, verbose: bool = True) -> str:
    """Interface simples."""
    agente = criar_agente(verbose=verbose)
    return agente.invocar(pergunta)


# ========== MODO INTERATIVO ==========

def teste_interativo():
    """Loop interativo."""
    
    print("\n" + "="*70)
    print("MODO INTERATIVO - Agente Investigador de Armas")
    print("="*70)
    
    print("\n📋 Exemplos:")
    print("- 'Existem furtos de Taurus?'")
    print("- 'Quantos portes válidos há?'")
    print("- 'Sair': exit, sair, quit")
    print("\n" + "="*70 + "\n")
    
    agente = criar_agente(verbose=True)
    
    while True:
        pergunta = input("\n🔍 Pergunta: ").strip()
        
        if pergunta.lower() in ["exit", "sair", "quit"]:
            print("\n👋 Até logo!")
            break
        
        if not pergunta:
            print("⚠️ Digite uma pergunta válida")
            continue
        
        try:
            resposta = agente.invocar(pergunta)
            print(f"\n✅ RESPOSTA FINAL:\n{resposta}\n")
        except Exception as e:
            print(f"\n❌ ERRO: {e}\n")


# ========== TESTES AUTOMÁTICOS ==========

def testes_automaticos():
    """Testes automáticos."""
    
    print("\n" + "="*70)
    print("TESTES AUTOMÁTICOS - ENCONTRO 1")
    print("="*70 + "\n")
    
    if not TOOLS_AVAILABLE:
        print("⚠️ Ferramentas não disponíveis\n")
    
    testes = [
        ("Existem furtos de Taurus?", ["furto", "Taurus"]),
        ("Quantos registros válidos?", ["registro", "válido"]),
    ]
    
    agente = criar_agente(verbose=False)
    passou = 0
    
    for i, (pergunta, esperado) in enumerate(testes, 1):
        print(f"[TEST {i}] {pergunta}")
        
        try:
            resposta = agente.invocar(pergunta)
            
            validado = all(termo.lower() in resposta.lower() for termo in esperado)
            status = "✅ PASSOU" if validado else "⚠️ PARCIAL"
            
            print(f"{status}")
            print(f"Resposta: {resposta[:100]}...\n")
            
            if validado:
                passou += 1
        except Exception as e:
            print(f"❌ ERRO: {e}\n")
    
    print(f"RESULTADO: {passou}/{len(testes)} testes\n")


# ========== DEMONSTRAÇÃO ==========

def demonstracao():
    """Demonstração."""
    
    print("\n" + "="*70)
    print("DEMONSTRAÇÃO - Agente ReAct Manual")
    print("="*70 + "\n")
    
    agente = criar_agente(verbose=True)
    
    perguntas = [
        "Existem furtos de arma Taurus?",
    ]
    
    for pergunta in perguntas:
        print(f"\n{'='*70}")
        print(f"PERGUNTA: {pergunta}")
        print('='*70)
        
        try:
            resposta = agente.invocar(pergunta)
            print(f"\n{'='*70}")
            print("RESPOSTA FINAL:")
            print('='*70)
            print(resposta)
        except Exception as e:
            print(f"\n❌ ERRO: {e}")


# ========== MAIN ==========

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Agente ReAct Manual (LangChain 1.3.13+ com Ollama)"
    )
    parser.add_argument(
        "modo",
        nargs="?",
        default="demo",
        choices=["demo", "interativo", "testes"],
        help="Modo: demo, interativo, testes"
    )
    
    args = parser.parse_args()
    
    try:
        if args.modo == "demo":
            demonstracao()
        elif args.modo == "interativo":
            teste_interativo()
        elif args.modo == "testes":
            testes_automaticos()
    except KeyboardInterrupt:
        print("\n\n👋 Interrompido")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        sys.exit(1)
