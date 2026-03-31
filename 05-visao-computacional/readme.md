### Comandos úteis:
```
uv venv .venv --python 3.11.9
.\.venv\Scripts\activate

uv pip install cmake
uv pip install wheel
uv pip install torch torchvision scikit-learn scikit-image matplotlib timm
uv pip install fastapi gradio pydantic ipython jupyter dlib-bin
uv pip install opencv-python opencv-contrib-python
uv pip install openai
uv pip install ultralytics insightface onnxruntime-gpu -q
uv pip install transformers 
python -m ensurepip --upgrade
```

### Instalar/rodar Ollama:
```
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama run llama2
docker exec -it ollama ollama pull <model_name>
```