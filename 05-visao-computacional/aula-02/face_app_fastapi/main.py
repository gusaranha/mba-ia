"""
FastAPI Server - Visão Computacional
====================================
Expoe funções de processamento de imagem via API REST.

Endpoints:
  POST /detectar-faces    → funcao1: imagem → imagem
  POST /detectar-coords-faces    → funcao2: imagem → imagem + lista
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import base64
import numpy as np
from PIL import Image
import cv2
import dlib
from vllm import VLLM
from recfacial import RecFacial

obj_vllm = VLLM('192.168.15.60', vllm_model='cpatonn/Qwen3-Omni-30B-A3B-Instruct-AWQ-4bit', api_key='EMPTY')
dlib_face_detector = dlib.get_frontal_face_detector()
dlib_face_predictor = dlib.shape_predictor("../models/shape_predictor_68_face_landmarks.dat")
obj_rec_facial = RecFacial(dlib_face_detector, dlib_face_predictor, obj_vllm)

def bytes_para_array(conteudo: bytes) -> np.ndarray:
    imagem = Image.open(io.BytesIO(conteudo)).convert("RGB")
    return np.array(imagem)

def array_para_bytes(array: np.ndarray) -> bytes:
    imagem = Image.fromarray(array.astype(np.uint8))
    buffer = io.BytesIO()
    imagem.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()

# ─────────────────────────────────────────────
# APP FASTAPI
# ─────────────────────────────────────────────

app = FastAPI(
    title="API de Visão Computacional",
    description="Endpoints para demonstração em aula de pós-graduação.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return {"mensagem": "API de Visão Computacional funcionando!",
            "endpoints": ["/detectar-faces", "/detectar-coords-faces", "/docs"]}


@app.post(
    "/detectar-faces",
    summary="Imagem → Imagem_anotada",
    response_description="Imagem processada em formato PNG",
)
async def detectar_faces(arquivo: UploadFile = File(..., description="Imagem de entrada (JPG, PNG, etc.)")):
    if not arquivo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")

    conteudo = await arquivo.read()
    imagem_np = bytes_para_array(conteudo)
    coord_faces, pontos = obj_rec_facial.obter_coordenadas_faces(imagem_np)
    img_decorada = obj_rec_facial.obter_imagem_faces_destacadas(imagem_np, coord_faces)

    bytes_saida = array_para_bytes(img_decorada)
    return StreamingResponse(io.BytesIO(bytes_saida), media_type="image/png")


@app.post(
    "/detectar-coords-faces",
    summary="Imagem → Imagem_anotada + [Coordenadas]",
)
async def detectar_coords_faces(arquivo: UploadFile = File(..., description="Imagem de entrada (JPG, PNG, etc.)")):
    if not arquivo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")

    conteudo = await arquivo.read()
    imagem_np = bytes_para_array(conteudo)
    coord_faces, pontos = obj_rec_facial.obter_coordenadas_faces(imagem_np)
    if coord_faces:
        img_decorada = obj_rec_facial.obter_imagem_faces_destacadas(imagem_np, coord_faces, pontos)
    else:
        img_decorada = imagem_np
    
    bytes_saida = array_para_bytes(img_decorada)
    imagem_b64 = base64.b64encode(bytes_saida).decode("utf-8")
    resp = JSONResponse({
        "imagem_base64": imagem_b64,
        "coordenadas": coord_faces,
    })

    return resp

@app.post(
    "/detectar-descrever",
    summary="Imagem → Imagem_anotada + [Coordenada, Face, Descricao]",
)
async def detectar_descrever_faces(arquivo: UploadFile = File(..., description="Imagem de entrada (JPG, PNG, etc.)"), 
                                   prompt: str = Form(default=None), ):
    if not arquivo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")

    print('server prompt:', prompt)
    conteudo = await arquivo.read()
    imagem_np = bytes_para_array(conteudo)
    coord_faces, pontos = obj_rec_facial.obter_coordenadas_faces(imagem_np)
    lst_img_faces = []
    descr_faces = []
    if coord_faces:
        img_decorada = obj_rec_facial.obter_imagem_faces_destacadas(imagem_np, coord_faces)
        lst_img_faces = obj_rec_facial.obter_imagens_faces(imagem_np, coord_faces)
        for face in lst_img_faces:
            descr = obj_rec_facial.descrever_face(face, prompt)
            descr_faces.append(descr)
    else:
        img_decorada = imagem_np

    bytes_saida = array_para_bytes(img_decorada)
    imagem_b64 = base64.b64encode(bytes_saida).decode("utf-8")
    lst_faces_descritas = []
    for img_face, coords, descr in zip(lst_img_faces, coord_faces, descr_faces):
        bytes_face = array_para_bytes(img_face)
        img_face_b64 = base64.b64encode(bytes_face).decode("utf-8")
        lst_faces_descritas.append({"face": img_face_b64, "coords": coords, "descr": descr})

    resp = JSONResponse({
        "imagem_base64": imagem_b64,
        "faces_descritas": lst_faces_descritas,
    })

    return resp


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
