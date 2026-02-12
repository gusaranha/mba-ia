python3 -m venv .venv
pip install -r requirements.txt
ollama pull nomic-embed-text
ollama pull qwen3-embedding
python -m uvicorn main3-2:app --reload