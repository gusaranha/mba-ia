from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import pathlib


model = YOLO("yolov8n.pt")
# Variantes disponíveis (crescente em precisão/custo):
#   yolov8n.pt (nano   com ~3M params  e 160 fps)
#   yolov8s.pt (small  com ~11M params e 120 fps)
#   yolov8m.pt (medium com ~25M params e  80 fps)
#   yolov8l.pt (large  com ~43M params e  50 fps)
#   yolov8x.pt (extra  com ~68M params e  30 fps)
# O arquivo .pt é baixado automaticamente se não existir localmente.

print("Classes do modelo COCO (80 classes):")
print(model.names)

def detectar_imagem(caminho_imagem, conf=0.25):
    path_imagem = pathlib.Path(caminho_imagem)
    resultados = model.predict(source=caminho_imagem, conf=conf, iou=0.45, imgsz=640, verbose=False,)
    classes_detectadas = []
    for result in resultados:
        print(60*"-")
        print(f"Imagem: {path_imagem.name}")
        print(f"Shape:  {result.orig_shape}")
        print(f"Objetos detectados: {len(result.boxes)}")
        print(60*"-")
        # os resultados são retângulos (bounding box) das detecções
        for retang in result.boxes:
            cls_id   = int(retang.cls[0])
            cls_nome = result.names[cls_id]
            classes_detectadas.append(cls_nome)
            conf_val = float(retang.conf[0])
            x1, y1, x2, y2 = retang.xyxy[0].tolist()
            cx, cy, w, h = retang.xywhn[0].tolist()
            print(f"  [{cls_id:2d}] {cls_nome:<15}  conf={conf_val:.2%}  bbox=[{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}]")

    num_deteccoes = len(classes_detectadas)
    num_classes_detectadas = len(set(classes_detectadas))
    return resultados, num_deteccoes, num_classes_detectadas


def visualizar_resultado(resultados, num_det, caminho_imagem, titulo="Detecção", saida="output/deteccao_yolo.png"):
    fig, ax = plt.subplots(1, 1, figsize=(9, 6))
    img_bgr = cv2.imread(caminho_imagem)
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    ax.imshow(img)
    cores = plt.cm.Set1(np.linspace(0, 1, max(num_det, 1)))
    for result in resultados:
        for retang in result.boxes:
            cls_id   = int(retang.cls[0])
            cls_nome = result.names[cls_id]
            conf = float(retang.conf[0])
            x1, y1, x2, y2 = retang.xyxy[0].cpu().numpy().astype(int)
            color = cores[cls_id % len(cores)]
            # retangulo deteccao
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=2.5, edgecolor=color, facecolor="none"
            )
            ax.add_patch(rect)
            # rótulo com confiança
            ax.text(
                x1, y1 - 6, f"{cls_nome} {conf:.2f}",
                color="white", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor=color, alpha=0.8)
            )
    
    ax.set_title(f"{titulo}\n{num_det} deteccoes", fontsize=10, pad=12)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(saida, dpi=120, bbox_inches="tight")
    plt.show()


def detectar_apenas_pessoas(caminho, conf=0.3):
    resultados = model.predict(source=caminho, classes=[0], conf=conf, verbose=False)
    num_det = 0
    for result in resultados:
        for box in result.boxes:
            num_det += 1
    print(60*"-")
    print(f"Pessoas detectadas: {num_det}")
    return resultados, num_det


if __name__ == "__main__":
    print(f"Argumentos passados: {sys.argv[1:]}")
    if len(sys.argv[1:]) == 0:
        print("informe pelo menos o nome de um arquivo")
    else:
        for str_path in sys.argv[1:]:
            path = pathlib.Path(str_path)
            if path.exists:
                caminho_imagem = str(path.absolute())
                resultados, num_det, num_cls = detectar_imagem(caminho_imagem, conf=0.25)
                visualizar_resultado(resultados, num_det, caminho_imagem, titulo="Detecção todos objetos", saida="output/det_objetos.png")
                resultados, num_det = detectar_apenas_pessoas(caminho_imagem)
                visualizar_resultado(resultados, num_det, caminho_imagem, titulo="Detecção de pessoas", saida="output/det_pessoas.png")
            else:
                print(f"Arquivo nao encontrado: {str_path}")



