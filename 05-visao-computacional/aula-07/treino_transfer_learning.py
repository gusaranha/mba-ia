from ultralytics import YOLO

yolo_custom = YOLO('yolov8n.pt')   # usa modelo pré-treinado para as classes do dataset COCO

projeto = "transfer_v1_ep30"
nome_modelo = "yolo_transfer"
path_config_yaml = 'config.yaml'

results_treino = yolo_custom.train(
    data=path_config_yaml,
    epochs=30,            # em projetos reais, voce deve usar mais de 100 epocas
    imgsz=640,
    batch=8,
    device='cpu',         
    project=projeto,
    name=nome_modelo,
    exist_ok=True,
    patience=15,
    plots=True,
    verbose=False,
    amp=True,            # desabilitar AMP em CPU
)

# depois de finalizado o treinamento... pegamos o melhor modelo
melhor_modelo = YOLO(f'runs/detect/{projeto}/{nome_modelo}/weights/best.pt')
# obtem dados de validacao
metrics = melhor_modelo.val(data=path_config_yaml, verbose=False)

print()
print()
print(60*'-')
print('Métricas validacao')
print(60*'-')
print(f'  mAP@0.50        : {metrics.box.map50:.4f}')
print(f'  mAP@0.50:0.95   : {metrics.box.map:.4f}')
print(f'  Precisao (mean) : {metrics.box.mp:.4f}')
print(f'  Recall (mean)   : {metrics.box.mr:.4f}')
print(60*'-')
for i, cls_idx in enumerate(metrics.box.ap_class_index):
    nome = melhor_modelo.names[cls_idx]
    ap   = metrics.box.ap50[i]
    print(f'  {int(cls_idx)} {nome:<15} AP@50 = {ap:.4f}')

