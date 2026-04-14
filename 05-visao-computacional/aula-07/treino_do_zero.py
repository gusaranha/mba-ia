from ultralytics import YOLO

"""
Organizacao do dataset

A estrutura padrao é:

dataset/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/


Você também pode ter um diretorio de testes:
dataset/
├── images/
│   ├── train/
│   └── val/
│   └── test/
└── labels/
    ├── train/
    └── val/
    └── test/

Uma forma alternativa de organizar os dados é iniciar com as particoes e internamente
criar os diretorios images e labels:

dataset/
├── train/
│   ├── images/
│   └── labels/
└── val/
    ├── images/
    └── labels/

os diretorios val e test são opcionais - MAS SAO ALTAMENTE RECOMENDADOS
                                       > o de validacao no processo de treino
                                       > o de teste no processo de avaliação final do treino

"""
# pata treinar do zero, escolha o modelo com extensão .yaml em vez de .pt
yolo_custom = YOLO("yolov8n.yaml")

projeto = "dozero_v1_ep30"
nome_modelo = "yolo_dozero"
# O arquivo de configuracao .yaml que será passado no argumento data 
# vai especificar as pastas usadas no processo de treino, bem como os rótulos do dataset
path_config_yaml = 'config.yaml'

results_treino = yolo_custom.train(data=path_config_yaml, epochs=30, project=projeto, name=nome_modelo)

print()
print()
print(60*'-')
print("pasta onde o YOLO salvou tudo:\n > ", end='')
print(results_treino.save_dir)
print("dicionário com as métricas finais de validação:\n > ", end='')
print(results_treino.results_dict)
print("mAP@50 final:\n > ", end='')
print(results_treino.box.map50)
print("mAP@50:95 final:\n > ", end='')
print(results_treino.box.map)
print("precisão por classe:\n > ", end='')
print(results_treino.box.p)  # precisao
print("recall por classe:\n > ", end='')
print(results_treino.box.r)  # recall

print()