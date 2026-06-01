# Usa uma imagem oficial do Python super leve
FROM python:3.11-slim

# Instala as bibliotecas geoespaciais do sistema (GDAL, PROJ, GEOS)
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Configura a pasta de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o resto do código
COPY . .