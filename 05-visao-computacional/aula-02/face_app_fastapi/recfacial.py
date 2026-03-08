import cv2
from PIL import Image
import numpy as np
import io
import base64
import re
import json

class RecFacial:

    def __init__(self, dlib_face_detector, dlib_face_predictor, vllm):
        self.dlib_face_detector = dlib_face_detector
        self.dlib_face_predictor = dlib_face_predictor
        self.vllm = vllm


    def obter_coordenadas_faces(self, img_rgb, force_upscale=True):
        scale = 1
        if force_upscale and max(img_rgb.shape[0:2])<1000:
            scale = 1.5
            img_rgb = self._resize_image_cv2(img_rgb, max_dimensao=int(scale*max(img_rgb.shape[0:2])))
                                                
        img_pb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        rects = self.dlib_face_detector(img_pb, 0)
        coords = []
        pontos = []
        for (i, rect) in enumerate(rects):
            shape = self.dlib_face_predictor(img_pb, rect)
            (x1, y1, x2, y2) = shape.rect.left(), shape.rect.top(), shape.rect.right(), shape.rect.bottom ()
            face_pts = []
            for p in shape.parts(): face_pts.append((int(p.x/scale), int(p.y/scale)))
            coords.append((int(x1/scale), int(y1/scale), int(x2/scale), int(y2/scale)))
            pontos.append(face_pts)

        coords, pontos = zip(*sorted(zip(coords, pontos), key=lambda el: el[0]))
        return coords, pontos


    def obter_imagem_faces_destacadas(self, img_rgb, coords, pontos=None):
        img_decorada = img_rgb.copy()
        if coords and not pontos: pontos = [[]]*len(coords)
        for i, (face_coords, face_points) in enumerate(zip(coords, pontos)):
            (x1,y1,x2,y2) = face_coords
            cv2.rectangle(img_decorada, (x1, y1), (x2, y2), (0, 255, 0), 2)
            for (x, y) in face_points:
                cv2.circle(img_decorada, (x, y), 2, (255, 255, 0), -1)

        return img_decorada


    def obter_imagens_faces(self, img_rgb, coords):
        lst_img_faces = []
        for _idx, fc in enumerate(coords, start=1):
            (x1,y1,x2,y2) = fc
            delta_y = (y2-y1)*0.25
            delta_x = (x2-x1)*0.25
            x1 = int(max(x1 - delta_x, 0))
            x2 = int(min(x2 + delta_x, img_rgb.shape[1]))
            y1 = int(max(y1 - delta_y, 0))
            y2 = int(min(y2 + delta_y, img_rgb.shape[0]))
            lst_img_faces.append(img_rgb[y1:y2, x1:x2])

        return lst_img_faces
    

    def descrever_face(self, img_rgb, prompt=None):
        img_pil = Image.fromarray(img_rgb)
        buffer = io.BytesIO()
        img_pil.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        if not prompt:
            prompt = """Atue como um sistema especialista em análise demográfica e reconhecimento facial. 
    Sua tarefa é analisar a imagem fornecida e extrair a idade e o sexo da pessoa.

    INSTRUÇÕES CRÍTICAS:
    1. Se a pessoa for anônima, e isso é mais provável, forneça uma estimativa numérica baseada em traços visuais.
    2. Se tiver certeza de que a pessoa é uma figura pública, mencione o nome dela nas observações.
    3. A saída deve ser estritamente um objeto JSON único, sem textos introdutórios ou conclusões.
    4. As observações devem ser sucintas, com no máximo 25 palavras.

    FORMATO DE RESPOSTA (EXEMPLO):
    {"idade": 18, "sexo": "Feminino", "observacoes": "Aparentemente trata-se da atriz inglesa Abigail Zoe Lewis."}

    PERGUNTA: Qual a idade e sexo da pessoa nessa foto, considerando que estamos em fevereiro de 2026?"""

        resp = self.vllm.get_resposta(img_b64, prompt)
        match = re.search(r'(\{.*\})', resp, re.DOTALL)
        descr = ''
        if match:
            json_str = match.group(1)
            dados = json.loads(json_str)
            keys = list(dados.keys())
            for k in keys:
                if k.lower() not in dados:
                    dados[k.lower()] = dados[k]
                    del dados[k]

            for k in ('idade', 'sexo', 'observacoes'):
                if k in dados:
                    descr += f"{k.title()}: {dados[k]}\n"
                    del dados[k]

            for k in dados:
                descr += f"{k.title()}: {dados[k]}\n"

            descr = descr.strip()

        else:
            descr = resp 

        return descr


    def _resize_image_cv2(self, img_np_rgb, max_dimensao=None, dimensao_exata=None, 
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
        
        # o metodo resize requer (largura, altura) - diferente da ordem do shape
        img_redim = cv2.resize(img_np_rgb, (nova_largura, nova_altura), interpolation=inter)
        if pad:
            vert_border = (max_dimensao - nova_altura) // 2
            horiz_border = (max_dimensao - nova_largura) // 2
            img_redim = cv2.copyMakeBorder(img_redim, vert_border, vert_border, horiz_border, horiz_border, 
                                            cv2.BORDER_CONSTANT, value=pad_color)
        return img_redim


