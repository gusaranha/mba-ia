"""Gera a configuração com os caminhos absolutos do ambiente do aluno."""
import json
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
arquivo = base / "opencode.json"
config = json.loads(arquivo.read_text(encoding="utf-8")) if arquivo.exists() else {"$schema": "https://opencode.ai/config.json"}
config.setdefault("mcp", {})["loja"] = {"type": "local", "command": [sys.executable, str(base / "servidor_mcp.py")], "enabled": True}
arquivo.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Configuração pronta: {arquivo}")
