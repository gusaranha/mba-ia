import cv2
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import base64
from openai import OpenAI


def show_image(
        img, size=None, cmap=None, axis='off', titulos=None
):
    img_list = [img] if not isinstance(img, list) else img
    if titulos and not isinstance(titulos, list): titulos = [titulos]
    num_images = len(img_list)
    if size is None: size = (5 * num_images, 5)
    fig, axes = plt.subplots(1, num_images, figsize=size)
    if num_images == 1: axes = [axes]
    for i, image in enumerate(img_list):
        axes[i].imshow(image, cmap=cmap)
        axes[i].axis(axis)
        if titulos and i < len(titulos): axes[i].set_title(titulos[i])
            
    plt.tight_layout()
    plt.show()

def resize_image_pil(
        img_pil, max_dimensao=None, dimensao_exata=None, 
        resample=Image.LANCZOS, pad=False, pad_color=(0, 0, 0)
):
    if max_dimensao is None and dimensao_exata is None: return img_pil
    if dimensao_exata is not None:
        max_dimensao = max(dimensao_exata)
        nova_largura, nova_altura = dimensao_exata
    else:
        largura, altura = img_pil.size
        nova_largura = nova_altura = max_dimensao
        if largura > altura: nova_altura = int(nova_largura * (altura / largura))
        elif altura > largura: nova_largura = int(nova_altura * (largura / altura))
    
    img_redim = img_pil.resize((nova_largura, nova_altura), resample=resample)
    if pad: img_redim = ImageOps.pad(img_redim, (max_dimensao, max_dimensao), color=pad_color)
    return img_redim

def resize_image_cv2(
        img_np_rgb, max_dimensao=None, dimensao_exata=None, 
        inter=cv2.INTER_AREA, pad=False, pad_color=(0, 0, 0)
):
    if max_dimensao is None and dimensao_exata is None: return img_np_rgb
    if dimensao_exata is not None:
        max_dimensao = max(dimensao_exata)
        nova_altura, nova_largura = dimensao_exata
    else:
        altura, largura = img_np_rgb.shape[0:2]
        nova_largura = nova_altura = max_dimensao
        if largura > altura: nova_altura = int(nova_largura * (altura / largura))
        elif altura > largura: nova_largura = int(nova_altura * (largura / altura))
    
    # o metodo resize do cv2 requer (largura, altura) - diferente da ordem do shape
    img_redim = cv2.resize(img_np_rgb, (nova_largura, nova_altura), interpolation=inter)
    if pad:
        vert_border = (max_dimensao - nova_altura) // 2
        horiz_border = (max_dimensao - nova_largura) // 2
        img_redim = cv2.copyMakeBorder(img_redim, vert_border, vert_border, horiz_border, horiz_border, 
                                        cv2.BORDER_CONSTANT, value=pad_color)
    return img_redim

def get_cliente_openai(host='localhost:11434', api_key=None):
    if api_key is None:
        if 'localhost' in host or '127.0.0.1'in host or '0.0.0.0' in host:
            api_key = "ollama"
        else:
            api_key = "EMPTY"
            
    client_openai_local = OpenAI(
        base_url=f"http://{host}/v1",
        api_key=api_key,
    )
    return client_openai_local

def get_resposta_vml(image_path, cliente, model, pergunta, answer_json=False):
    base64_image = None
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as ex:
        print("Erro codificando imagem:", ex)
        return None

    if model is None:
        models = []
        for model_data in cli.models.list().model_dump()['data']:
            if model_data['object'] == 'model':
                models.append(model_data['id'])
        if models: model = models[0]
        else: return None

    messages = []
    if answer_json:
        messages = [
            {
                "role": "system",
                "content": "Você é um extrator de dados JSON. Responda apenas com o objeto JSON solicitado, sem markdown ou explicações."
            },
        ]

    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": pergunta},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                },
            ],
        })

    response = cliente.chat.completions.create(
        model=model,
        messages=messages,
    )

    return response.choices[0].message.content