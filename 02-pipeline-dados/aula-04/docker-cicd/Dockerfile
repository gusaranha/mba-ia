# ==================================================
# DOCKERFILE - Calculadora de Score de Crédito
# ==================================================

# 1️⃣ IMAGEM BASE
FROM python:3.11-slim

# 2️⃣ CRIAR PASTA DE TRABALHO
WORKDIR /app

# 3️⃣ COPIAR DEPENDÊNCIAS E INSTALAR
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4️⃣ COPIAR CÓDIGO
COPY . .

# 5️⃣ COMANDO PADRÃO (rodar calculadora)
CMD ["python", "calculadora.py"]

# ==================================================
# COMO USAR:
# 
# Construir:
#   docker build -t calculadora-score .
#
# Rodar:
#   docker run calculadora-score
#
# Rodar testes:
#   docker run calculadora-score pytest test_calculadora.py -v
# ==================================================
