# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las herramientas necesarias para crear el entorno virtual y las dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-venv \
    libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea el entorno virtual dentro del contenedor
RUN python -m venv /app/venv

# Usa el entorno virtual para instalar pip, las dependencias del proyecto y Sentry SDK
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r requirements.txt
RUN /app/venv/bin/pip install sentry-sdk

# Expone el puerto donde correrá la aplicación
EXPOSE 8000

# Comando para correr la aplicación utilizando el entorno virtual
CMD ["/app/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
