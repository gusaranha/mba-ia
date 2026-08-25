### git version
```
(venv_rag) gustavoaranha@Gustavos-iMac local % git --version
git version 2.50.1 (Apple Git-155)
```

### python version
```
(aula-01) gustavoaranha@Gustavos-iMac aula-01 % python --version
Python 3.11.9
```

### docker version
```
gustavoaranha@Gustavos-iMac local % docker --version
Docker version 29.7.2, build a7dcaa6
```

### azure version
```
gustavoaranha@Gustavos-iMac local % az --version
azure-cli                         2.89.1

core                              2.89.1
telemetry                          1.1.0

Dependencies:
msal                              1.36.0
azure-mgmt-resource               24.0.0

Python location '/usr/local/Cellar/azure-cli/2.89.1/libexec/bin/python'
Config directory '/Users/gustavoaranha/.azure'
Extensions directory '/Users/gustavoaranha/.azure/cliextensions'

Python (Darwin) 3.14.6 (main, Jun 10 2026, 10:03:53) [Clang 17.0.0 (clang-1700.6.4.2)]

Legal docs and information: aka.ms/AzureCliLegal
```

### demo_ml_1_sem_preprocessamento.py
```
(aula-01) gustavoaranha@Gustavos-iMac aula-01 % python demo_ml_1_sem_preprocessamento.py
============================================================
RESULTADO — SEM pré-processamento cuidadoso
============================================================
Acurácia:  50.00%
Precisão:  47.92%
Revocação: 50.00%
F1-Score:  46.67%

Problemas introduzidos de propósito neste script:
- idade_vitima faltante virou 0 (parece um recém-nascido registrando um BO)
- outlier de R$ 480.000 não foi tratado
- 'bairro' (nominal) recebeu Label Encoding, criando uma ordem falsa
- texto não foi normalizado (maiúsculas/minúsculas tratadas como diferentes)
- variáveis numéricas em escalas muito diferentes, sem padronização
```

### demo_ml_2_com_preprocessamento.py 
```
(aula-01) gustavoaranha@Gustavos-iMac aula-01 % python demo_ml_2_com_preprocessamento.py 
============================================================
RESULTADO — COM pré-processamento
============================================================
Acurácia:  66.67%
Precisão:  73.61%
Revocação: 66.67%
F1-Score:  63.89%

O que foi corrigido em relação ao script 1:
- idade_vitima faltante: imputada com a mediana + flag indicando imputação
- outlier de prejuízo: limitado (clip) pelo método do IQR
- idade fora da faixa plausível: limitada a 10-100 anos
- 'bairro' (nominal) → One-Hot Encoding | 'turno' (ordinal) → Label Encoding com ordem certa
- texto normalizado (minúsculas, sem pontuação, sem stopwords) antes do TF-IDF
- variáveis numéricas padronizadas (StandardScaler) antes do treino
```
