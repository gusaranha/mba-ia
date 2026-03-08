# Cliente Gradio - Visão Computacional
# Interface web interativa para consumir a API FastAPI.
# 
# Como usar:
#   1. Inicie o servidor:  python server.py
#   2. Inicie o cliente:   python client_gradio.py
#   3. Acesse no browser:  http://localhost:7860

import gradio as gr
import requests
import base64
import numpy as np
from PIL import Image
import io

API_URL = "http://localhost:8000"

def detectar_faces(imagem_np: np.ndarray):
    if imagem_np is None:
        return None, "Por favor, envie uma imagem."

    # Converte numpy array → bytes PNG
    pil_img = Image.fromarray(imagem_np.astype(np.uint8))
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)

    try:
        response = requests.post(
            f"{API_URL}/detectar-faces",
            files={"arquivo": ("imagem.png", buffer, "image/png")},
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return None, f"Não foi possível conectar à API em {API_URL}.\nVerifique se o servidor está rodando."
    except requests.exceptions.HTTPError as e:
        return None, f"Erro da API: {e}\n{response.text}"

    imagem_saida = Image.open(io.BytesIO(response.content)).convert("RGB")
    return np.array(imagem_saida), "Processamento concluído com sucesso!"


def detectar_coords_faces(imagem_np: np.ndarray):
    if imagem_np is None:
        return None, None, "Por favor, envie uma imagem."

    pil_img = Image.fromarray(imagem_np.astype(np.uint8))
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)

    try:
        response = requests.post(
            f"{API_URL}/detectar-coords-faces",
            files={"arquivo": ("imagem.png", buffer, "image/png")},
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return None, None, f"Não foi possível conectar à API em {API_URL}.\nVerifique se o servidor está rodando."
    except requests.exceptions.HTTPError as e:
        return None, None, f"Erro da API: {e}\n{response.text}"

    dados = response.json()

    # Decodifica imagem Base64
    print('decode base64')
    img_bytes = base64.b64decode(dados["imagem_base64"])
    print('imagem anotada')
    imagem_anotada = np.array(Image.open(io.BytesIO(img_bytes)).convert("RGB"))
    print(imagem_anotada.shape)
    # Formata detecções em tabela
    coordenadas = dados.get("coordenadas", [])
    print('coordenadas')

    qtd_faces = 0
    if coordenadas:
        qtd_faces = len(coordenadas)
        linhas = ''
        for _idx, c in enumerate(coordenadas, start=1):
            linhas += f"Face {_idx}: {c}\n"
        tabela = linhas.strip()
    else:
        tabela = [{"resultado": "Nenhuma face detectada"}]

    msg = f"{qtd_faces} faces(s) detectado(s)!"
    print(imagem_anotada.shape, tabela, msg)
    return imagem_anotada, tabela, msg


def detectar_descrever_faces(imagem_np: np.ndarray, prompt=None):
    """Chama /detectar-descrever e monta os componentes dinâmicos de exibição."""
    if imagem_np is None:
        return None, "", "Por favor, envie uma imagem."

    pil_img = Image.fromarray(imagem_np.astype(np.uint8))
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)
    print(prompt)
    try:
        response = requests.post(
            f"{API_URL}/detectar-descrever",
            files={"arquivo": ("imagem.png", buffer, "image/png")},
            data={"prompt": prompt},
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return None, "", f"Não foi possível conectar à API em {API_URL}."
    except requests.exceptions.HTTPError as e:
        return None, "", f"Erro da API: {e}\n{response.text}"

    dados = response.json()

    # Imagem anotada
    img_bytes = base64.b64decode(dados["imagem_base64"])
    imagem_anotada = np.array(Image.open(io.BytesIO(img_bytes)).convert("RGB"))

    # Monta HTML dos cards com face + coords + descrição
    faces_descritas = dados.get("faces_descritas", [])
    if not faces_descritas:
        html = "<p style='color:gray'>Nenhuma face detectada.</p>"
    else:
        cards_html = ""
        for idx, item in enumerate(faces_descritas, start=1):
            img_b64  = item["face"]
            coords   = item["coords"]
            descr    = item["descr"].replace("\n", "<br>")
            cards_html += f"""
            <div style="
                display:inline-block; vertical-align:top;
                border:1px solid #ddd; border-radius:10px;
                padding:12px; margin:8px; width:200px;
                background:#fafafa; box-shadow: 2px 2px 6px #ccc;
                font-family: monospace; font-size: 13px;
            ">
                <div style="font-weight:bold; margin-bottom:6px; color:#333">
                    Face {idx}
                </div>
                <img src="data:image/png;base64,{img_b64}"
                     style="width:100%; border-radius:6px; margin-bottom:8px"/>
                <div style="color:#555; margin-bottom:4px">
                    {coords}
                </div>
                <div style="color:#222">
                    {descr}
                </div>
            </div>"""
        html = f"<div style='display:flex; flex-wrap:wrap;'>{cards_html}</div>"

    qtd = len(faces_descritas)
    return imagem_anotada, gr.HTML(value=html), f"{qtd} face(s) detectada(s) e descrita(s)!"


def checar_api():
    """Verifica se a API está acessível."""
    try:
        r = requests.get(f"{API_URL}/", timeout=5)
        r.raise_for_status()
        return f"API online em {API_URL}"
    except Exception:
        return f"API offline — inicie o servidor em {API_URL}"


# ─────────────────────────────────────────────
# INTERFACE GRADIO
# ─────────────────────────────────────────────

css = """
.gradio-container { font-family: 'IBM Plex Mono', monospace; }
.status-box { font-size: 0.9em; padding: 6px 12px; border-radius: 6px; }
"""

with gr.Blocks(
    title="Visão Computacional — Demo API",
    theme=gr.themes.Default(
        primary_hue="blue",
        neutral_hue="slate",
    ),
    css=css,
) as demo:

    # ── Cabeçalho ──────────────────────────────
    gr.Markdown("""
    # 🔭 Visão Computacional
    **Execução via FastAPI**
    
    Faça upload de uma imagem e veja os dois endpoints em ação.
    """)

    status_box = gr.Textbox(
        label="Status da API",
        value=checar_api(),
        interactive=False,
        elem_classes="status-box",
    )
    gr.Button("Verificar conexão", size="sm").click(fn=checar_api, outputs=status_box)

    gr.Markdown("---")

    # EP1
    with gr.Tab("EP1 — Destacar Faces"):
        gr.Markdown("""
        ### `POST /detectar-faces`
        Recebe uma imagem e retorna uma imagem c/ faces destacadas.
        """)
        with gr.Row():
            with gr.Column():
                img_entrada1 = gr.Image(label="Imagem de entrada", type="numpy")
                btn1 = gr.Button("> Enviar para a API", variant="primary")
            with gr.Column():
                img_saida1 = gr.Image(label="Imagem com anotações (deteccoes)")
                msg1 = gr.Textbox(label="Status", interactive=False)

        btn1.click(fn=detectar_faces, inputs=img_entrada1, outputs=[img_saida1, msg1])

    # EP2
    with gr.Tab("EP2 — Destacar Faces e Coords."):
        gr.Markdown("""
        ### `POST /detectar-coords-faces`
        Recebe uma imagem e retorna uma imagem c/ faces destacadas **+** coordenadas.
        """)
        with gr.Row():
            with gr.Column():
                img_entrada2 = gr.Image(label="Imagem de entrada", type="numpy")
                btn2 = gr.Button("> Enviar para a API", variant="primary")
            with gr.Column():
                img_saida2 = gr.Image(label="Imagem com anotações (deteccoes)")
                msg2 = gr.Textbox(label="Status", interactive=False)

        tabela = gr.Textbox(label="Coordenadas das faces")
        btn2.click(fn=detectar_coords_faces, inputs=img_entrada2, outputs=[img_saida2, tabela, msg2])

    # EP3
    with gr.Tab("EP3 — Detectar e Descrever Faces"):
        gr.Markdown("""
        ### `POST /detectar-descrever`
        Recebe uma imagem e retorna uma imagem c/ faces destacadas **+** (faces, coordenadas e descricoes).
        """)
        with gr.Row():
            with gr.Column():
                img_entrada3 = gr.Image(label="Imagem de entrada", type="numpy")
                btn3 = gr.Button("> Enviar para a API", variant="primary")
            with gr.Column():
                img_saida3 = gr.Image(label="Imagem anotada")
                msg3 = gr.Textbox(label="Status", interactive=False)

        cards_saida3 = gr.HTML(label="Faces detectadas")
        btn3.click(
            fn=detectar_descrever_faces,
            inputs=img_entrada3,
            outputs=[img_saida3, cards_saida3, msg3],
        )

    # endpoint 3
    with gr.Tab("EP3 — Detectar e Descrever Face Cust."):
        gr.Markdown("""
        ### `POST /detectar-descrever`
        Recebe uma imagem e retorna uma imagem c/ faces destacadas **+** (faces, coordenadas e descricoes).
        """)
        with gr.Row():
            with gr.Column():
                img_entrada4 = gr.Image(label="Imagem de entrada", type="numpy")
                txt_prompt = gr.Text(label="Prompt descricao:", interactive=True)
                btn4 = gr.Button("> Enviar para a API", variant="primary")
            with gr.Column():
                img_saida4 = gr.Image(label="Imagem anotada")
                msg4 = gr.Textbox(label="Status", interactive=False)

        cards_saida4 = gr.HTML(label="Faces detectadas")
        btn4.click(
            fn=detectar_descrever_faces,
            inputs=[img_entrada4, txt_prompt],
            outputs=[img_saida4, cards_saida4, msg4],
        )

    # sobre
    with gr.Tab("Sobre"):
        gr.Markdown(f"""
        ### Como funciona
        
        ```
        ┌─────────────┐    HTTP POST     ┌──────────────────┐
        │  Gradio UI  │ ───────────────► │  FastAPI Server  │
        │  (cliente)  │ ◄─────────────── │  (server.py)     │
        └─────────────┘   JSON / PNG     └──────────────────┘
        ```
        
        | EP             | Função     | Entrada  | Saída               |
        |-----------------------|------------|----------|---------------------|
        | `/detectar-faces`   | `funcao1`  | imagem   | imagem              |
        | `/detectar-coords-faces`   | `funcao2`  | imagem   | imagem + lista      |
        
        ### Documentação interativa da API
        Acesse **[{API_URL}/docs]({API_URL}/docs)** para explorar os endpoints via Swagger UI.
        
        ### Instalação
        ```bash
        pip install fastapi uvicorn gradio pillow numpy opencv-python requests
        ```
        """)

# ─────────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
