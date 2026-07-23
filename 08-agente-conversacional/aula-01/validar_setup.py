#!/usr/bin/env python3
"""
🔍 VALIDADOR DE SETUP - E1 ANATOMIA DO AGENTE
Valida se todo o ambiente está configurado corretamente para a aula

Uso:
    python validar_setup.py

Resultado:
    - ✅ se está ok
    - ❌ se tem erro
    - Gera setup_report.json para professor revisar
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Imprime cabeçalho bonito"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║          🔍 VALIDADOR DE SETUP - E1                       ║")
    print("║          Anatomia do Agente - ReAct + LangChain           ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")

def print_test(name: str, status: bool, message: str = ""):
    """Imprime resultado de um teste"""
    icon = f"{Colors.GREEN}✅{Colors.RESET}" if status else f"{Colors.RED}❌{Colors.RESET}"
    msg = f" - {message}" if message else ""
    print(f"{icon} {name}{msg}")
    return status

def test_python_version() -> Tuple[bool, Dict]:
    """Testa versão Python"""
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    required = (3, 9)
    
    if sys.version_info >= required:
        print_test("Python versão", True, f"v{version}")
        return True, {"version": version, "status": "OK"}
    else:
        print_test("Python versão", False, f"v{version} (requer 3.9+)")
        return False, {"version": version, "status": "ERRO", "error": "Python 3.9+ requerido"}

def test_langchain() -> Tuple[bool, Dict]:
    """Testa se LangChain está instalado"""
    try:
        import langchain
        version = langchain.__version__
        print_test("LangChain", True, f"v{version}")
        return True, {"version": version, "status": "OK"}
    except ImportError as e:
        print_test("LangChain", False, "Não instalado")
        return False, {"status": "ERRO", "error": str(e)}

def test_langchain_ollama() -> Tuple[bool, Dict]:
    """Testa se langchain_ollama está instalado"""
    try:
        from langchain_ollama import OllamaLLM
        print_test("LangChain Ollama", True, "Importado")
        return True, {"status": "OK"}
    except ImportError as e:
        print_test("LangChain Ollama", False, "Não instalado")
        return False, {"status": "ERRO", "error": str(e)}

def test_ollama_running() -> Tuple[bool, Dict]:
    """Testa se Ollama está rodando"""
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
        print_test("Ollama daemon", True, "Rodando em localhost:11434")
        return True, {"status": "OK", "url": "http://localhost:11434"}
    except Exception as e:
        print_test("Ollama daemon", False, "Não conectado (execute: ollama serve)")
        return False, {"status": "ERRO", "error": "Ollama não está rodando"}

def test_ollama_llm_connection() -> Tuple[bool, Dict]:
    """Testa conexão com LLM via Ollama"""
    try:
        from langchain_ollama import OllamaLLM
        
        llm = OllamaLLM(model="llama3")
        
        # Testa com prompt rápido
        response = llm.invoke("test")
        
        if response:
            print_test("LLM (llama3)", True, "Respondendo corretamente")
            return True, {"status": "OK", "model": "llama3"}
        else:
            print_test("LLM (llama3)", False, "Não respondeu")
            return False, {"status": "ERRO", "error": "LLM não respondeu"}
            
    except Exception as e:
        print_test("LLM (llama3)", False, "Erro na conexão")
        return False, {"status": "ERRO", "error": str(e)}

def test_ollama_models() -> Tuple[bool, Dict]:
    """Testa quais modelos estão disponíveis"""
    try:
        import json
        import urllib.request
        
        response = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
        data = json.loads(response.read().decode())
        
        models = [model["name"] for model in data.get("models", [])]
        
        if "llama3" in [m.split(":")[0] for m in models]:
            print_test("Modelos disponíveis", True, f"{len(models)} modelos (llama3 ok)")
            return True, {"models": models, "status": "OK"}
        else:
            print_test("Modelos disponíveis", False, f"llama3 não encontrado (encontrados: {models})")
            return False, {"models": models, "status": "AVISO", "error": "llama3 não disponível"}
            
    except Exception as e:
        print_test("Modelos disponíveis", False, "Não conseguiu listar")
        return False, {"status": "ERRO", "error": str(e)}

def test_disk_space() -> Tuple[bool, Dict]:
    """Testa espaço em disco"""
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_gb = free / (1024**3)
        
        if free_gb > 1:  # Mínimo 1GB
            print_test("Espaço em disco", True, f"{free_gb:.1f} GB disponível")
            return True, {"free_gb": free_gb, "status": "OK"}
        else:
            print_test("Espaço em disco", False, f"Apenas {free_gb:.1f} GB (mínimo 1GB)")
            return False, {"free_gb": free_gb, "status": "AVISO"}
            
    except Exception as e:
        print_test("Espaço em disco", False, "Não conseguiu verificar")
        return False, {"status": "AVISO", "error": str(e)}

def run_all_tests() -> Dict:
    """Executa todos os testes"""
    print_header()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    all_passed = True
    
    # Teste 1: Python
    print(f"{Colors.BOLD}1. Ambiente Python{Colors.RESET}")
    passed, data = test_python_version()
    results["tests"]["python"] = data
    all_passed = all_passed and passed
    
    # Teste 2: LangChain
    print(f"\n{Colors.BOLD}2. Bibliotecas instaladas{Colors.RESET}")
    passed, data = test_langchain()
    results["tests"]["langchain"] = data
    all_passed = all_passed and passed
    
    passed, data = test_langchain_ollama()
    results["tests"]["langchain_ollama"] = data
    all_passed = all_passed and passed
    
    # Teste 3: Ollama
    print(f"\n{Colors.BOLD}3. Ollama daemon{Colors.RESET}")
    passed, data = test_ollama_running()
    results["tests"]["ollama_daemon"] = data
    all_passed = all_passed and passed
    
    if passed:  # Só testa LLM se Ollama está rodando
        print(f"\n{Colors.BOLD}4. Modelos e conexão LLM{Colors.RESET}")
        
        passed_models, data = test_ollama_models()
        results["tests"]["ollama_models"] = data
        
        passed_llm, data = test_ollama_llm_connection()
        results["tests"]["ollama_llm"] = data
        all_passed = all_passed and passed_llm
    
    # Teste 4: Disco
    print(f"\n{Colors.BOLD}5. Recursos do sistema{Colors.RESET}")
    passed, data = test_disk_space()
    results["tests"]["disk_space"] = data
    
    # Resultado final
    results["overall_status"] = "PRONTO" if all_passed else "ERROS_ENCONTRADOS"
    
    return results, all_passed

def print_summary(results: Dict, all_passed: bool):
    """Imprime resumo final"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    
    if all_passed:
        print("║          ✅ SETUP 100% PRONTO PARA AULA!               ║")
    else:
        print("║          ❌ SETUP COM ERROS - VER ACIMA                 ║")
    
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    # Dicas
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ Você está 100% pronto para terça-feira!{Colors.RESET}")
        print("\nPróximos passos:")
        print("  1. Leia: CICLO_REACT_VISUAL.md")
        print("  2. Responda: CHECKPOINT_PRE_AULA.md")
        print("  3. Segunda: Repita validador se reiniciar PC")
        print("  4. Terça: Traga computador ligado e pronto!\n")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Erros encontrados. Siga os passos acima para resolver.{Colors.RESET}")
        print("\nComuns:")
        print("  - 'Ollama não conectado': Execute 'ollama serve' em outro terminal")
        print("  - 'ModuleNotFoundError': Execute 'pip install -r requirements.txt'")
        print("  - 'llama3 não encontrado': Execute 'ollama pull llama3'\n")

def save_report(results: Dict, filename: str = "setup_report.json"):
    """Salva relatório em JSON"""
    report_path = Path(filename)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório salvo em: {report_path.absolute()}")
    print(f"   (Envie este arquivo para o professor)")

if __name__ == "__main__":
    try:
        results, all_passed = run_all_tests()
        print_summary(results, all_passed)
        save_report(results)
        
        # Exit code
        sys.exit(0 if all_passed else 1)
        
    except Exception as e:
        print(f"\n{Colors.RED}❌ Erro inesperado:{Colors.RESET}")
        print(f"   {e}")
        sys.exit(1)
